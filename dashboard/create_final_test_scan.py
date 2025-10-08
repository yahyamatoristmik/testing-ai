import os
import sys
import django
from datetime import datetime

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, Repository, UserSCMProfile
from django.contrib.auth.models import User
from django.utils import timezone

def create_final_test_scan():
    print("🎯 CREATING FINAL TEST SCAN")
    print("=" * 50)
    
    # Get test data
    user = User.objects.get(username='sast_test_user')
    scm_profile = UserSCMProfile.objects.get(user=user, scm_type='github')
    repository = Repository.objects.filter(scm_profile=scm_profile).first()
    
    if not repository:
        print("❌ No repository found")
        return
    
    # Create new scan
    scan = ScanJob.objects.create(
        user=user,
        repository=repository,
        branch='final-test-branch',
        status='queued',
        triggered_at=timezone.now()
    )
    
    print(f"✅ SCAN #{scan.id} CREATED")
    print(f"   - Repository: {repository.name}")
    print(f"   - Branch: {scan.branch}")
    print(f"   - Status: {scan.status}")
    print(f"   - User: {user.username}")
    
    return scan.id

if __name__ == '__main__':
    scan_id = create_final_test_scan()
    print(f"\n💡 Scan #{scan_id} is ready for processing!")
    print("   Start the worker to see it in action.")
