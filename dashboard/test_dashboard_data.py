import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport, Repository
from django.db.models import Count

def test_dashboard_data():
    print("📊 TESTING DASHBOARD DATA")
    print("=" * 60)
    
    # Data untuk dashboard
    total_scans = ScanJob.objects.count()
    completed_scans = ScanJob.objects.filter(status='completed').count()
    running_scans = ScanJob.objects.filter(status='running').count()
    pending_scans = ScanJob.objects.filter(status='pending').count()
    
    total_vulns = VulnerabilityReport.objects.count()
    high_vulns = VulnerabilityReport.objects.filter(severity='HIGH').count()
    medium_vulns = VulnerabilityReport.objects.filter(severity='MEDIUM').count()
    
    repositories = Repository.objects.count()
    
    print("📈 DASHBOARD STATISTICS:")
    print(f"   - Total Scans: {total_scans}")
    print(f"   - Completed: {completed_scans}")
    print(f"   - Running: {running_scans}") 
    print(f"   - Pending: {pending_scans}")
    print(f"   - Total Vulnerabilities: {total_vulns}")
    print(f"   - High: {high_vulns}")
    print(f"   - Medium: {medium_vulns}")
    print(f"   - Repositories: {repositories}")
    
    # Recent scans
    print(f"\n🕒 RECENT SCANS:")
    recent_scans = ScanJob.objects.select_related('repository').order_by('-id')[:5]
    for scan in recent_scans:
        vuln_count = VulnerabilityReport.objects.filter(scan_job=scan).count()
        print(f"   - Scan #{scan.id}: {scan.repository.name} - {scan.status} (Findings: {vuln_count})")
    
    # Check if views will see this data
    print(f"\n🔍 WILL THIS APPEAR IN DASHBOARD?")
    if total_scans > 0 and total_vulns > 0:
        print("   ✅ YES - Data exists and should appear in dashboard")
    else:
        print("   ❌ NO - Need to create test data")

if __name__ == '__main__':
    test_dashboard_data()
