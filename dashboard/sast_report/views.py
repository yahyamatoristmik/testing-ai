from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Count, Q
import threading
from .models import SCMProfile, Repository, ScanJob, Finding
from .services.scan_service import SimpleScanService
from .decorators import sast_permission_required, sast_access_required

def check_sast_access(user):
    """Utility function untuk check SAST access"""
    if user.is_superuser:
        return True
        
    sast_permissions = [
        'sast_report.can_view_sast',
        'sast_report.can_manage_scm',
        'sast_report.can_run_scan', 
        'sast_report.can_view_reports'
    ]
    
    return any(user.has_perm(perm) for perm in sast_permissions)

# === DASHBOARD ===
@sast_access_required()
@login_required  
def dashboard(request):
    """Dashboard SAST utama - Hanya untuk user dengan SAST permission"""
    if not check_sast_access(request.user):
        messages.error(request, "❌ Access denied. You don't have permission to access SAST Security Scanner.")
        return redirect('home')  # Ganti dengan URL home Anda
    
    scm_profiles = SCMProfile.objects.filter(user=request.user, is_active=True)
    repositories = Repository.objects.filter(scm_profile__user=request.user, is_active=True)
    recent_scans = ScanJob.objects.filter(repository__scm_profile__user=request.user).select_related('repository')[:10]
    
    # Hitung statistik
    total_scans = ScanJob.objects.filter(repository__scm_profile__user=request.user).count()
    completed_scans = ScanJob.objects.filter(
        repository__scm_profile__user=request.user, 
        status='completed'
    ).count()
    
    # Hitung findings by severity
    severity_stats = {}
    for severity in ['critical', 'high', 'medium', 'low', 'info']:
        severity_stats[severity] = Finding.objects.filter(
            scan_job__repository__scm_profile__user=request.user,
            severity=severity
        ).count()
    
    context = {
        'scm_profiles': scm_profiles,
        'repositories': repositories,
        'recent_scans': recent_scans,
        'total_scans': total_scans,
        'completed_scans': completed_scans,
        'severity_stats': severity_stats,
    }
    return render(request, 'sast_report/dashboard.html', context)

# === SCM PROFILES === 
@sast_permission_required('sast_report.can_manage_scm')
@login_required
def scm_profiles(request):
    """Kelola SCM Profiles - Hanya untuk user dengan manage permission"""
    if not request.user.has_perm('sast_report.can_manage_scm'):
        messages.error(request, "❌ Access denied. You need 'Can manage SCM profiles' permission.")
        return redirect('sast_report:dashboard')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            scm_type = request.POST.get('scm_type')
            token = request.POST.get('token')
            username = request.POST.get('username', '')
            
            if not scm_type or not token:
                messages.error(request, "SCM type and token are required")
                return redirect('sast_report:scm_profiles')
            
            profile = SCMProfile.objects.create(
                user=request.user,
                scm_type=scm_type,
                token=token,
                username=username
            )
            messages.success(request, f"✅ {scm_type} profile added successfully!")
            
        elif action == 'update':
            profile_id = request.POST.get('profile_id')
            token = request.POST.get('token')
            
            profile = get_object_or_404(SCMProfile, id=profile_id, user=request.user)
            profile.token = token
            profile.save()
            messages.success(request, f"✅ {profile.scm_type} token updated!")
            
        elif action == 'delete':
            profile_id = request.POST.get('profile_id')
            profile = get_object_or_404(SCMProfile, id=profile_id, user=request.user)
            profile.delete()
            messages.success(request, "✅ SCM profile deleted!")
        
        return redirect('sast_report:scm_profiles')
    
    profiles = SCMProfile.objects.filter(user=request.user)
    return render(request, 'sast_report/scm_profiles.html', {'profiles': profiles})

# === REPOSITORIES ===
@sast_permission_required('sast_report.can_view_sast')
@login_required
def repositories(request):
    """Daftar Repositories - Hanya untuk user dengan view permission"""
    if not request.user.has_perm('sast_report.can_view_sast'):
        messages.error(request, "❌ Access denied. You need 'Can view SAST dashboard' permission.")
        return redirect('home')
    
    repositories = Repository.objects.filter(
        scm_profile__user=request.user, 
        is_active=True
    ).select_related('scm_profile')
    
    for repo in repositories:
        repo.total_scans = ScanJob.objects.filter(repository=repo).count()
        repo.last_scan = ScanJob.objects.filter(repository=repo).order_by('-created_at').first()
    
    context = {
        'repositories': repositories,
    }
    return render(request, 'sast_report/repositories.html', context)

# === START SCAN ===
@sast_permission_required('sast_report.can_run_scan')
@login_required
def start_scan(request, repo_id):
    """Start scan untuk repository - Hanya untuk user dengan run permission"""
    if not request.user.has_perm('sast_report.can_run_scan'):
        messages.error(request, "❌ Access denied. You need 'Can run security scans' permission.")
        return redirect('sast_report:repositories')
    
    repository = get_object_or_404(Repository, id=repo_id, scm_profile__user=request.user)
    
    scan_job = ScanJob.objects.create(
        repository=repository,
        branch=repository.default_branch
    )
    
    def run_scan():
        try:
            scan_service = SimpleScanService(scan_job)
            scan_service.run_scan()
        except Exception as e:
            scan_job.status = 'failed'
            scan_job.error_message = f"Background error: {str(e)}"
            scan_job.completed_at = timezone.now()
            scan_job.save()
    
    thread = threading.Thread(target=run_scan)
    thread.daemon = True
    thread.start()
    
    messages.success(request, f"🚀 Scan started for {repository.name}")
    return redirect('sast_report:scan_results', scan_id=scan_job.id)

# === SCAN RESULTS ===
@sast_permission_required('sast_report.can_view_reports')
@login_required
def scan_results(request, scan_id):
    """Lihat hasil scan - Hanya untuk user dengan view reports permission"""
    if not request.user.has_perm('sast_report.can_view_reports'):
        messages.error(request, "❌ Access denied. You need 'Can view scan reports' permission.")
        return redirect('sast_report:dashboard')
    
    scan_job = get_object_or_404(
        ScanJob, 
        id=scan_id, 
        repository__scm_profile__user=request.user
    )
    findings = Finding.objects.filter(scan_job=scan_job)
    
    severity_counts = {
        'critical': findings.filter(severity='critical').count(),
        'high': findings.filter(severity='high').count(),
        'medium': findings.filter(severity='medium').count(),
        'low': findings.filter(severity='low').count(),
        'info': findings.filter(severity='info').count(),
    }
    
    context = {
        'scan_job': scan_job,
        'findings': findings,
        'severity_counts': severity_counts,
        'total_findings': sum(severity_counts.values()),
    }
    return render(request, 'sast_report/scan_results.html', context)

# === SCAN HISTORY ===
@sast_permission_required('sast_report.can_view_reports')
@login_required
def scan_history(request):
    """Riwayat scan - Hanya untuk user dengan view reports permission"""
    if not request.user.has_perm('sast_report.can_view_reports'):
        messages.error(request, "❌ Access denied. You need 'Can view scan reports' permission.")
        return redirect('sast_report:dashboard')
    
    scans = ScanJob.objects.filter(
        repository__scm_profile__user=request.user
    ).select_related('repository', 'repository__scm_profile').order_by('-created_at')[:50]
    
    stats = ScanJob.objects.filter(
        repository__scm_profile__user=request.user
    ).aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='completed')),
        running=Count('id', filter=Q(status='running')),
        failed=Count('id', filter=Q(status='failed')),
        pending=Count('id', filter=Q(status='pending'))
    )
    
    context = {
        'scans': scans,
        'total_scans': stats['total'] or 0,
        'completed_scans': stats['completed'] or 0,
        'running_scans': stats['running'] or 0,
        'failed_scans': stats['failed'] or 0,
        'pending_scans': stats['pending'] or 0,
    }
    return render(request, 'sast_report/scan_history.html', context)

# === SCAN STATUS API ===
@sast_permission_required('sast_report.can_view_reports')
@login_required
def scan_status_api(request, scan_id):
    """API untuk real-time scan status - Hanya untuk user dengan view permission"""
    if not request.user.has_perm('sast_report.can_view_reports'):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    scan_job = get_object_or_404(
        ScanJob, 
        id=scan_id, 
        repository__scm_profile__user=request.user
    )
    
    return JsonResponse({
        'status': scan_job.status,
        'log': scan_job.scan_log,
        'error': scan_job.error_message,
        'findings_count': scan_job.total_findings,
        'duration': scan_job.get_duration_display(),
    })
