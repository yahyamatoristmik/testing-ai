import os
import sys
import django
import time

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport, UserSCMProfile
from django.contrib.auth.models import User

def test_complete_workflow():
    print("🎯 COMPLETE SAST WORKFLOW TEST")
    print("=" * 60)
    
    # Step 1: Create test data
    print("\n1. 🔧 SETTING UP TEST DATA")
    user, created = User.objects.get_or_create(
        username='workflow_test_user',
        defaults={'email': 'workflow@test.com', 'password': 'test123'}
    )
    if created:
        print("   ✅ Created test user")
    
    scm_profile, created = UserSCMProfile.objects.get_or_create(
        user=user,
        defaults={
            'scm_type': 'github',
            'access_token': 'test-token-workflow',
            'username': 'workflow-user'
        }
    )
    if created:
        print("   ✅ Created SCM profile")
    
    # Step 2: Create multiple scan jobs
    print("\n2. 🚀 CREATING SCAN JOBS")
    repositories = [
        'https://github.com/workflow-user/api-service.git',
        'https://github.com/workflow-user/web-app.git',
        'https://github.com/workflow-user/mobile-app.git'
    ]
    
    scan_ids = []
    for repo in repositories:
        scan = ScanJob.objects.create(
            user=user,
            scm_profile=scm_profile,
            repository_url=repo,
            target_branch='main',
            status='queued'
        )
        scan_ids.append(scan.id)
        print(f"   ✅ Created scan #{scan.id}: {repo}")
    
    # Step 3: Show initial status
    print("\n3. 📊 INITIAL STATUS")
    queued_count = ScanJob.objects.filter(status='queued').count()
    total_vulns = VulnerabilityReport.objects.count()
    print(f"   - Queued scans: {queued_count}")
    print(f"   - Total vulnerabilities in system: {total_vulns}")
    
    # Step 4: Monitor progress (simulate)
    print("\n4. ⏳ WORKFLOW READY")
    print("   The worker will automatically process these scans:")
    for scan_id in scan_ids:
        scan = ScanJob.objects.get(id=scan_id)
        print(f"      - Scan #{scan_id}: {scan.repository_url}")
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS:")
    print("   1. Keep 'python3 start_worker_fixed.py' running")
    print("   2. Worker will automatically pick up queued scans")
    print("   3. Check dashboard for real-time progress")
    print("   4. Run 'python3 test_progress_fixed.py' to monitor")
    
    return scan_ids

if __name__ == '__main__':
    test_complete_workflow()
