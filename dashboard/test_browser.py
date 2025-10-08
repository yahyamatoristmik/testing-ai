import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport

def check_browser_data():
    print("🌐 DATA UNTUK BROWSER")
    print("=" * 50)
    
    print("📊 Data yang akan muncul di browser:")
    print(f"   Total Scans: {ScanJob.objects.count()}")
    print(f"   Completed: {ScanJob.objects.filter(status='completed').count()}")
    print(f"   Running: {ScanJob.objects.filter(status='running').count()}")
    print(f"   High Vulnerabilities: {VulnerabilityReport.objects.filter(severity='HIGH').count()}")
    print(f"   Medium Vulnerabilities: {VulnerabilityReport.objects.filter(severity='MEDIUM').count()}")
    
    print("\n🔍 Recent Scans:")
    for scan in ScanJob.objects.all().order_by('-id')[:3]:
        print(f"   - Scan #{scan.id}: {scan.repository.name} ({scan.status}) - Findings: {scan.findings_count}")
    
    print("\n💡 Buka https://sentinel.investpro.id/sast-report/ di browser")
    print("   Jika masih kosong, masalahnya di:")
    print("   1. Template base.html (extends/missing blocks)")
    print("   2. Static files (CSS/JS)")
    print("   3. Authentication middleware")

if __name__ == '__main__':
    check_browser_data()
