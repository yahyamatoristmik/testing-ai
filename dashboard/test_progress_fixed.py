import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport, Sast

def test_scan_system():
    print("🔍 SCAN SYSTEM STATUS")
    print("====================")
    
    # Scan Jobs
    scan_jobs = ScanJob.objects.all()
    print(f"\n📊 SCAN JOBS: {scan_jobs.count()} total")
    
    for status in ['queued', 'in_progress', 'completed', 'failed']:
        count = scan_jobs.filter(status=status).count()
        print(f"   - {status.upper()}: {count}")
    
    # Vulnerability Reports
    vuln_reports = VulnerabilityReport.objects.all()
    print(f"\n⚠️  VULNERABILITY REPORTS: {vuln_reports.count()} total")
    
    for severity in ['critical', 'high', 'medium', 'low', 'info']:
        count = vuln_reports.filter(severity=severity).count()
        if count > 0:
            print(f"   - {severity.upper()}: {count}")
    
    # Latest scan details
    latest_scan = scan_jobs.order_by('-created_at').first()
    if latest_scan:
        print(f"\n📋 LATEST SCAN (#{latest_scan.id}):")
        print(f"   - Repository: {latest_scan.repository_url}")
        print(f"   - Status: {latest_scan.status}")
        print(f"   - Created: {latest_scan.created_at}")
        
        if latest_scan.status == 'completed':
            vulns = vuln_reports.filter(scan_job=latest_scan)
            print(f"   - Vulnerabilities found: {vulns.count()}")
    
    # SAST models
    sast_scans = Sast.objects.all()
    print(f"\n🔧 SAST SCANS: {sast_scans.count()}")

if __name__ == '__main__':
    test_scan_system()
