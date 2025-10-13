from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DataLeakConfig, DataLeakScan, UserDataLeakPermission
from .forms import DataLeakScanForm
import requests
import json

def has_data_leak_access(user):
    if user.is_superuser:
        return True
    try:
        permission = UserDataLeakPermission.objects.get(user=user)
        return permission.can_access_data_leak
    except UserDataLeakPermission.DoesNotExist:
        return False

def is_data_leak_active():
    try:
        config = DataLeakConfig.objects.first()
        return config.is_active if config else False
    except:
        return False

@login_required
def data_leak_dashboard(request):
    if not has_data_leak_access(request.user):
        messages.error(request, "You don't have permission to access Data Leak features.")
        return redirect('admin:index')
    
    if not is_data_leak_active():
        messages.error(request, "Data Leak feature is currently disabled.")
        return redirect('admin:index')
    
    scans = DataLeakScan.objects.filter(requested_by=request.user).order_by('-created_at')[:10]
    form = DataLeakScanForm()
    
    context = {
        'form': form,
        'scans': scans,
    }
    return render(request, 'data_leak/dashboard.html', context)

@login_required
def submit_scan(request):
    if not has_data_leak_access(request.user):
        messages.error(request, "Permission denied")
        return redirect('admin:index')
    
    if not is_data_leak_active():
        messages.error(request, "Data Leak feature is disabled")
        return redirect('admin:index')
    
    if request.method == 'POST':
        form = DataLeakScanForm(request.POST)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.requested_by = request.user
            scan.save()
            
            # Simulate scan process
            scan.status = 'completed'
            scan.results = '{"leaks_found": 0, "status": "clean"}'
            scan.save()
            
            messages.success(request, f"Scan for {scan.target} completed successfully.")
            return redirect('data_leak:dashboard')
    
    messages.error(request, "Invalid scan request.")
    return redirect('data_leak:dashboard')

@login_required
def scan_history(request):
    if not has_data_leak_access(request.user):
        messages.error(request, "You don't have permission to access Data Leak features.")
        return redirect('admin:index')
    
    scans = DataLeakScan.objects.filter(requested_by=request.user).order_by('-created_at')
    
    context = {
        'scans': scans,
    }
    return render(request, 'data_leak/history.html', context)

@login_required
def scan_detail(request, scan_id):
    if not has_data_leak_access(request.user):
        messages.error(request, "You don't have permission to access Data Leak features.")
        return redirect('admin:index')
    
    scan = get_object_or_404(DataLeakScan, id=scan_id, requested_by=request.user)
    
    context = {
        'scan': scan,
    }
    return render(request, 'data_leak/scan_detail.html', context)
