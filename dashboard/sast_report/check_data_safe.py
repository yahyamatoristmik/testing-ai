import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport

def check_data_safe():
    print("📊 SAFE DATA CHECK (NO SCAN_DURATION)")
    print("=" * 50)
    
    # Gunakan values() untuk hindari scan_duration field
    scans = ScanJob.objects.all().values('id', 'status', 'repository_id', 'findings_count', 'high_count', 'medium_count')[:10]
    
    print(f"🔍 LATEST SCANS (safe query):")
    for scan in scans:
        vuln_count = VulnerabilityReport.objects.filter(scan_job_id=scan['id']).count()
        print(f"   - Scan #{scan['id']}: {scan['status']} | Findings: {vuln_count}")
    
    # Overall stats
    print(f"\n📈 OVERALL STATISTICS:")
    print(f"   - Total Scans: {ScanJob.objects.count()}")
    print(f"   - Total Vulnerabilities: {VulnerabilityReport.objects.count()}")
    
    # Status breakdown
    status_counts = ScanJob.objects.values('status').annotate(count=models.Count('id'))
    print(f"\n🔍 STATUS BREAKDOWN:")
    for item in status_counts:
        print(f"   - {item['status'].upper()}: {item['count']}")

if __name__ == '__main__':
    check_data_safe()
