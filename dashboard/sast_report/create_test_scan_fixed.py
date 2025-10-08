import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, Repository, UserSCMProfile
from django.contrib.auth.models import User
from django.utils import timezone

def create_test_scan():
    print("🎯 CREATING TEST SCAN (FIXED)")
    print("=" * 50)
    
    # Get user dan repository
    user = User.objects.first()
    repository = Repository.objects.first()
    
    if not repository:
        print("❌ No repository found")
        return
    
    # Create scan dengan status 'pending' (sesuai model)
    scan = ScanJob.objects.create(
        user=user,
        repository=repository,
        branch='main',
        status='pending',  # SESUAI MODEL
        triggered_at=timezone.now()
    )
    
    print(f"✅ SCAN #{scan.id} CREATED")
    print(f"   - Repository: {repository.name}")
    print(f"   - Status: {scan.status}")
    print(f"   - User: {user.username}")
    
    return scan.id

if __name__ == '__main__':
    scan_id = create_test_scan()
    print(f"\n💡 Scan #{scan_id} is ready! Worker will process it.")
