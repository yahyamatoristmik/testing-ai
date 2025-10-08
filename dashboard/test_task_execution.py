import os
import django
import tempfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, Repository, UserSCMProfile
from django.contrib.auth.models import User
from sast_report.tasks import run_semgrep_scan

def test_task_execution():
    print("🧪 TESTING TASK EXECUTION IN DJANGO CONTEXT")
    
    user = User.objects.get(username='admin')
    scm_profile = UserSCMProfile.objects.get(user=user, scm_type='gitlab')
    repository = Repository.objects.filter(scm_profile=scm_profile).first()
    
    # Buat scan job
    scan_job = ScanJob.objects.create(
        user=user,
        repository=repository,
        branch='main',
        status='pending'
    )
    
    print(f"🎯 Created scan job #{scan_job.id}")
    print(f"📦 Repository: {repository.name}")
    
    # Jalankan task langsung (synchronous)
    print("\n🚀 EXECUTING RUN_SEMGREP_SCAN TASK...")
    try:
        run_semgrep_scan(scan_job.id)
        
        # Reload scan job untuk melihat hasil
        scan_job.refresh_from_db()
        print(f"📊 Final status: {scan_job.status}")
        print(f"📝 Log: {scan_job.log}")
        
        if scan_job.status == 'completed':
            print("✅ TASK EXECUTION SUCCESSFUL")
        else:
            print(f"❌ TASK EXECUTION FAILED: {scan_job.log}")
            
    except Exception as e:
        print(f"❌ TASK EXECUTION ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_task_execution()
