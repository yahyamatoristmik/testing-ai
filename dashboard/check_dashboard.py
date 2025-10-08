import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

def test_dashboard_urls():
    print("🔍 TESTING DASHBOARD URLS")
    print("=" * 50)
    
    client = Client()
    
    # Test various URLs
    urls_to_test = [
        '/sast-report/',
        '/dashboard/',
        '/scan-jobs/',
        '/vulnerabilities/',
        '/reports/'
    ]
    
    for url in urls_to_test:
        try:
            response = client.get(url)
            print(f"🌐 {url} - Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ Accessible")
            elif response.status_code == 302:
                print(f"   🔄 Redirect to: {response.url}")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"🌐 {url} - Exception: {e}")

def check_current_data():
    print("\n📊 CURRENT DATA IN DATABASE:")
    print("=" * 50)
    
    from sast_report.models import ScanJob, VulnerabilityReport, Repository
    
    # Scan Jobs
    scans = ScanJob.objects.all().order_by('-id')[:5]
    print(f"🔍 LATEST 5 SCAN JOBS:")
    for scan in scans:
        vuln_count = VulnerabilityReport.objects.filter(scan_job=scan).count()
        print(f"   - Scan #{scan.id}: {scan.status} (Vulns: {vuln_count}) - {scan.repository.name}")
    
    # Overall stats
    print(f"\n📈 OVERALL STATISTICS:")
    print(f"   - Total Scans: {ScanJob.objects.count()}")
    print(f"   - Queued: {ScanJob.objects.filter(status='queued').count()}")
    print(f"   - Completed: {ScanJob.objects.filter(status='completed').count()}")
    print(f"   - Vulnerabilities: {VulnerabilityReport.objects.count()}")

if __name__ == '__main__':
    test_dashboard_urls()
    check_current_data()
