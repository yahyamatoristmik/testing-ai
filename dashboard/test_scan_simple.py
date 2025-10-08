import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, Repository
from django.contrib.auth.models import User

def test_scan():
    print("🧪 TESTING SCAN SYSTEM")
    
    # Gunakan user admin yang sudah ada
    user = User.objects.get(username='admin')
    repository = Repository.objects.filter(scm_profile__user=user).first()
    
    if not repository:
        print("❌ No repositories found for admin user")
        return
    
    print(f"📦 Testing with repository: {repository.name}")
    
    # Buat scan job
    scan_job = ScanJob.objects.create(
        user=user,
        repository=repository,
        branch='main',
        status='running',
        log="Starting test scan...\n"
    )
    
    print(f"🎯 Created scan job #{scan_job.id}")
    
    try:
        # Simulate successful scan
        scan_job.status = 'completed'
        scan_job.findings_count = 3
        scan_job.critical_count = 1
        scan_job.high_count = 1  
        scan_job.medium_count = 1
        scan_job.log = "Test scan completed successfully.\nFound 3 security issues:\n- 1 Critical\n- 1 High\n- 1 Medium"
        scan_job.save()
        
        print("✅ Test scan completed successfully")
        print(f"📊 Found {scan_job.findings_count} security issues")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        scan_job.status = 'failed'
        scan_job.log = f"Test failed: {str(e)}"
        scan_job.save()

if __name__ == "__main__":
    test_scan()
