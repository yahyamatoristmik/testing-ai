from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
import json
from .models import DarkWebConfig, DarkWebScan, DarkWebFinding, UserDarkWebPermission
from .forms import DarkWebScanForm

@login_required
def darkweb_scan_detail(request, scan_id):
    if not has_darkweb_access(request.user):
        messages.error(request, "You don't have permission to access Dark Web Monitoring.")
        return redirect('admin:index')
    
    scan = get_object_or_404(DarkWebScan, id=scan_id, requested_by=request.user)
    findings = scan.findings.all()
    
    # Hitung risk level
    risk_counts = findings.values('risk_level').annotate(count=Count('risk_level'))
    risk_summary = {item['risk_level']: item['count'] for item in risk_counts}
    
    context = {
        'scan': scan,
        'findings': findings,
        'risk_summary': risk_summary,
    }
    return render(request, 'darkweb_monitor/scan_detail.html', context)

def has_darkweb_access(user):
    if user.is_superuser:
        return True
    try:
        permission = UserDarkWebPermission.objects.get(user=user)
        return permission.can_access_darkweb
    except UserDarkWebPermission.DoesNotExist:
        return False

def is_darkweb_active():
    try:
        config = DarkWebConfig.objects.first()
        return config.is_active if config else False
    except:
        return False

@login_required
def darkweb_dashboard(request):
    if not has_darkweb_access(request.user):
        messages.error(request, "You don't have permission to access Dark Web Monitoring.")
        return redirect('admin:index')
    
    if not is_darkweb_active():
        messages.error(request, "Dark Web Monitoring feature is currently disabled.")
        return redirect('admin:index')
    
    scans = DarkWebScan.objects.filter(requested_by=request.user).order_by('-created_at')[:10]
    form = DarkWebScanForm()
    
    # Statistics
    total_scans = scans.count()
    high_risk_findings = DarkWebFinding.objects.filter(scan__requested_by=request.user, risk_level__in=['high', 'critical']).count()
    
    context = {
        'form': form,
        'scans': scans,
        'total_scans': total_scans,
        'high_risk_findings': high_risk_findings,
    }
    return render(request, 'darkweb_monitor/dashboard.html', context)

@login_required
def submit_darkweb_scan(request):
    if not has_darkweb_access(request.user):
        messages.error(request, "Permission denied")
        return redirect('admin:index')
    
    if not is_darkweb_active():
        messages.error(request, "Dark Web Monitoring feature is disabled")
        return redirect('admin:index')
    
    if request.method == 'POST':
        form = DarkWebScanForm(request.POST)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.requested_by = request.user
            scan.save()
            
            # Start darkweb scan process - HAPUS .delay()
            perform_darkweb_scan(scan.id)
            
            messages.success(request, f"Dark Web scan for {scan.target} has been started.")
            return redirect('darkweb_monitor:dashboard')
    
    messages.error(request, "Invalid scan request.")
    return redirect('darkweb_monitor:dashboard')

@login_required
def darkweb_history(request):
    if not has_darkweb_access(request.user):
        messages.error(request, "You don't have permission to access Dark Web Monitoring.")
        return redirect('admin:index')
    
    scans = DarkWebScan.objects.filter(requested_by=request.user).order_by('-created_at')
    
    context = {
        'scans': scans,
    }
    return render(request, 'darkweb_monitor/history.html', context)

@login_required
def darkweb_scan_detail(request, scan_id):
    if not has_darkweb_access(request.user):
        messages.error(request, "You don't have permission to access Dark Web Monitoring.")
        return redirect('admin:index')
    
    scan = get_object_or_404(DarkWebScan, id=scan_id, requested_by=request.user)
    findings = scan.findings.all()
    
    context = {
        'scan': scan,
        'findings': findings,
    }
    return render(request, 'darkweb_monitor/scan_detail.html', context)

# Dark Web Scanning Functions
def check_haveibeenpwned(email, api_key=None):
    """Check email against Have I Been Pwned database"""
    try:
        headers = {}
        if api_key:
            headers['hibp-api-key'] = api_key
            
        response = requests.get(
            f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []  # No breaches found
        else:
            return None
            
    except Exception as e:
        print(f"HIBP Error: {e}")
        return None

def check_dehashed(query, api_key, email):
    """Check DeHashed database for compromised credentials"""
    try:
        auth = (email, api_key)
        response = requests.get(
            f'https://api.dehashed.com/search?query={query}',
            auth=auth,
            headers={'Accept': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
            
    except Exception as e:
        print(f"DeHashed Error: {e}")
        return None

def perform_darkweb_scan(scan_id):
    """Main function to perform darkweb scan - SYNC VERSION"""
    try:
        scan = DarkWebScan.objects.get(id=scan_id)
        config = DarkWebConfig.objects.first()
        
        if not config:
            scan.status = 'failed'
            scan.error_message = 'DarkWeb configuration not found'
            scan.save()
            return
        
        scan.status = 'running'
        scan.save()
        
        results = {
            'hibp_breaches': [],
            'dehashed_results': [],
            'risk_score': 0,
            'summary': {}
        }
        
        # Check Have I Been Pwned
        if config.hibp_api_key:
            hibp_results = check_haveibeenpwned(scan.target, config.hibp_api_key)
            if hibp_results:
                results['hibp_breaches'] = hibp_results
                for breach in hibp_results:
                    DarkWebFinding.objects.create(
                        scan=scan,
                        source='hibp',
                        finding_type='email_breach',
                        description=f"Email found in {breach.get('Name', 'Unknown')} breach",
                        risk_level='high' if breach.get('IsSensitive', False) else 'medium',
                        data_points=breach.get('PwnCount', 0),
                        breach_date=breach.get('BreachDate', None),
                        raw_data=breach
                    )
        
        # Check DeHashed
        if config.dehashed_api_key and config.dehashed_email:
            dehashed_results = check_dehashed(scan.target, config.dehashed_api_key, config.dehashed_email)
            if dehashed_results and dehashed_results.get('entries'):
                results['dehashed_results'] = dehashed_results['entries']
                for entry in dehashed_results['entries']:
                    DarkWebFinding.objects.create(
                        scan=scan,
                        source='dehashed',
                        finding_type='credential_leak',
                        description=f"Credential leak: {entry.get('email', 'N/A')}",
                        risk_level='critical' if entry.get('password') else 'high',
                        data_points=1,
                        raw_data=entry
                    )
        
        # Calculate risk score
        total_findings = scan.findings.count()
        critical_findings = scan.findings.filter(risk_level='critical').count()
        high_findings = scan.findings.filter(risk_level='high').count()
        
        risk_score = min(100, (critical_findings * 40) + (high_findings * 20) + (total_findings * 5))
        
        scan.results = results
        scan.risk_score = risk_score
        scan.status = 'completed'
        scan.save()
        
    except DarkWebScan.DoesNotExist:
        pass
    except Exception as e:
        scan.status = 'failed'
        scan.error_message = str(e)
        scan.save()
