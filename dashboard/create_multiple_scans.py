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
    
    # Create multiple repositories and scans
    test_repos = [
        {
            'name': 'API Service Repository',
            'url': 'https://github.com/testuser/api-service.git',
            'branch': 'main'
        },
        {
            'name': 'Web Application', 
            'url': 'https://github.com/testuser/web-app.git',
            'branch': 'develop'
        },
        {
            'name': 'Mobile Backend',
            'url': 'https://github.com/testuser/mobile-backend.git', 
            'branch': 'feature/auth'
        }
    ]
    
    created_scans = []
    
    for repo_data in test_repos:
        # Create repository
        repo, created = Repository.objects.get_or_create(
            scm_profile=scm_profile,
            name=repo_data['name'],
            defaults={
                'url': repo_data['url'],
                'description': f'Test repository: {repo_data["name"]}',
                'is_active': True
            }
        )
        
        # Create scan job
        scan = ScanJob.objects.create(
            user=user,
            repository=repo,
            branch=repo_data['branch'],
            status='queued',
            triggered_at=timezone.now()
        )
        
        created_scans.append(scan.id)
        print(f"✅ Created scan #{scan.id} for {repo_data['name']} ({repo_data['branch']})")
    
    print(f"\n🎯 TOTAL SCANS CREATED: {len(created_scans)}")
    print(f"📋 Scan IDs: {created_scans}")
    print("\n💡 Worker will automatically process these scans in order")

if __name__ == '__main__':
    create_multiple_scans()
