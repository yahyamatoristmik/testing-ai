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

def create_multiple_scans():
    print("🚀 CREATING MULTIPLE SCAN JOBS FOR TESTING")
    print("=" * 50)
    
    # Get existing test data
    user = User.objects.get(username='sast_test_user')
    scm_profile = UserSCMProfile.objects.get(user=user, scm_type='github')
    
    # Use existing repositories or create with unique names
    existing_repos = Repository.objects.filter(scm_profile=scm_profile)
    
    if existing_repos.exists():
        print("📁 USING EXISTING REPOSITORIES:")
        for repo in existing_repos:
            print(f"   - {repo.name}")
        
        # Create scans for existing repositories
        created_scans = []
        for repo in existing_repos:
            scan = ScanJob.objects.create(
                user=user,
                repository=repo,
                branch='test-branch',
                status='queued',
                triggered_at=timezone.now()
            )
            created_scans.append(scan.id)
            print(f"✅ Created scan #{scan.id} for {repo.name}")
        
        print(f"\n🎯 TOTAL SCANS CREATED: {len(created_scans)}")
        print(f"📋 Scan IDs: {created_scans}")
    
    else:
        print("❌ No existing repositories found")
        print("💡 Run create_complete_scan.py first to create test data")

if __name__ == '__main__':
    create_multiple_scans()
