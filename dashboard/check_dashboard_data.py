import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport

def check_dashboard_data():
    print("📊 DASHBOARD DATA CHECK")
    print("=" * 60)
    
    # Total statistics
    total_scans = ScanJob.objects.count()
    total_vulns = VulnerabilityReport.objects.count()
    
    print(f"📈 OVERALL STATISTICS:")
    print(f"   - Total Scans: {total_scans}")
    print(f"   - Total Vulnerabilities: {total_vulns}")
    
    # Scan status breakdown
    print(f"\n🔍 SCAN STATUS BREAKDOWN:")
    for status in ['queued', 'processing', 'done', 'completed', 'failed']:
        count = ScanJob.objects.filter(status=status).count()
        if count > 0:
            print(f"   - {status.upper()}: {count}")
    
    # Latest scans
    print(f"\n🕒 LATEST 5 SCANS:")
    latest_scans = ScanJob.objects.all().order_by('-id')[:5]
    for scan in latest_scans:
        vuln_count = VulnerabilityReport.objects.filter(scan_job=scan).count()
        print(f"   - Scan #{scan.id}: {scan.status} | Findings: {vuln_count} | {scan.repository.name}")
    
    # Vulnerability severity breakdown
    print(f"\n⚠️  VULNERABILITY SEVERITY:")
    for severity in ['critical', 'high', 'medium', 'low', 'info']:
        count = VulnerabilityReport.objects.filter(severity=severity).count()
        if count > 0:
            print(f"   - {severity.upper()}: {count}")

if __name__ == '__main__':
    check_dashboard_data()
