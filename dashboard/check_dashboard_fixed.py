import os
import sys
import django

# Setup Django FIRST
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

# Now import Django components
from django.test import Client
from django.contrib.auth.models import User
from sast_report.models import ScanJob, VulnerabilityReport

def test_dashboard_urls():
    print("🔍 TESTING DASHBOARD URLS")
    print("=" * 50)
    
    client = Client(HTTP_HOST='sentinel.investpro.id')  # Set correct host
    
    urls_to_test = [
        '/sast-report/',
        '/dashboard/',
        '/scan-jobs/',
        '/vulnerabilities/',
        '/'
    ]
    
    for url in urls_to_test:
        try:
            response = client.get(url, HTTP_HOST='sentinel.investpro.id')
            print(f"🌐 {url} - Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ Accessible")
                if hasattr(response, 'context_data'):
                    print(f"   📊 Context: {list(response.context_data.keys())}")
            elif response.status_code == 302:
                print(f"   🔄 Redirect to: {response.url}")
            else:
                print(f"   ❌ Error")
        except Exception as e:
            print(f"🌐 {url} - Exception: {e}")

def check_current_data():
    print("\n📊 CURRENT DATA IN DATABASE:")
    print("=" * 50)
    
    # Scan Jobs
    scans = ScanJob.objects.all().order_by('-id')[:10]
    print(f"🔍 LATEST SCAN JOBS:")
    for scan in scans:
        vuln_count = VulnerabilityReport.objects.filter(scan_job=scan).count()
        print(f"   - Scan #{scan.id}: {scan.status} | Vulns: {vuln_count} | {scan.repository.name}")
    
    # Overall stats
    print(f"\n📈 OVERALL STATISTICS:")
    print(f"   - Total Scans: {ScanJob.objects.count()}")
    print(f"   - Queued: {ScanJob.objects.filter(status='queued').count()}")
    print(f"   - Processing: {ScanJob.objects.filter(status='processing').count()}")
    print(f"   - Done: {ScanJob.objects.filter(status='done').count()}")
    print(f"   - Total Vulnerabilities: {VulnerabilityReport.objects.count()}")

if __name__ == '__main__':
    test_dashboard_urls()
    check_current_data()
