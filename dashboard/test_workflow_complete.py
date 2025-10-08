import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, Repository, VulnerabilityReport
from django.contrib.auth.models import User

def test_complete_workflow():
    print("🎯 COMPLETE SAST WORKFLOW TEST")
    print("=" * 60)
    
    # Step 1: Setup test data
    print("\n1. 🔧 SETTING UP TEST DATA")
    
    # User
    user, created = User.objects.get_or_create(
        username='workflow_test_user',
        defaults={'email': 'workflow@test.com', 'password': 'test123'}
    )
    if created:
        print("   ✅ Created test user")
    
    # Repository
    repo, created = Repository.objects.get_or_create(
        name='Workflow Test Repository',
        defaults={
            'url': 'https://github.com/workflow-user/test-repo.git',
            'description': 'Repository for workflow testing',
            'is_active': True
        }
    )
    if created:
        print("   ✅ Created test repository")
    
    # Step 2: Create scan jobs
    print("\n2. 🚀 CREATING SCAN JOBS")
    
    scan_ids = []
    branches = ['main', 'develop', 'feature/auth']
    
    for branch in branches:
        try:
            scan = ScanJob.objects.create(
                user=user,
                repository=repo,
                branch=branch,
                status='queued',
                triggered_at=timezone.now()
            )
            scan_ids.append(scan.id)
            print(f"   ✅ Created scan #{scan.id} for branch: {branch}")
        except Exception as e:
            print(f"   ❌ Failed to create scan for {branch}: {e}")
    
    # Step 3: Show initial status
    print("\n3. 📊 INITIAL STATUS")
    queued_count = ScanJob.objects.filter(status='queued').count()
    total_vulns = VulnerabilityReport.objects.count()
    print(f"   - Queued scans: {queued_count}")
    print(f"   - Total vulnerabilities in system: {total_vulns}")
    
    print("\n" + "=" * 60)
    print("🎯 WORKFLOW READY!")
    print("   The worker will automatically process these queued scans.")
    print(f"   Scan IDs: {scan_ids}")
    
    return scan_ids

if __name__ == '__main__':
    test_complete_workflow()
