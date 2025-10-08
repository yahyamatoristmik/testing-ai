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

def create_complete_test_data():
    """Create all necessary test data for a scan"""
    print("🔧 CREATING COMPLETE TEST DATA")
    print("=" * 50)
    
    # Step 1: Create or get user
    try:
        user = User.objects.get(username='sast_test_user')
        print("✅ Using existing user")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='sast_test_user',
            email='test@example.com',
            password='testpass123'
        )
        print("✅ Created new user")
    
    # Step 2: Create or get SCM profile
    try:
        scm_profile = UserSCMProfile.objects.get(user=user, scm_type='github')
        print("✅ Using existing SCM profile")
    except UserSCMProfile.DoesNotExist:
        scm_profile = UserSCMProfile.objects.create(
            user=user,
            scm_type='github',
            access_token='test-token-123456',
            username='testuser-github'
        )
        print("✅ Created new SCM profile")
    
    # Step 3: Create or get repository
    try:
        repository = Repository.objects.get(name='Test Repository', scm_profile=scm_profile)
        print("✅ Using existing repository")
    except Repository.DoesNotExist:
        repository = Repository.objects.create(
            scm_profile=scm_profile,
            name='Test Repository',
            url='https://github.com/testuser/test-repo.git',
            description='Test repository for SAST scanning',
            is_active=True
        )
        print("✅ Created new repository")
    
    return user, scm_profile, repository

def trigger_new_scan():
    print("🚀 TRIGGERING NEW SCAN JOB")
    print("=" * 50)
    
    # Create all necessary data
    user, scm_profile, repository = create_complete_test_data()
    
    # Create new scan job
    try:
        new_scan = ScanJob.objects.create(
            user=user,
            repository=repository,
            branch='main',
            status='queued',
            triggered_at=timezone.now()
        )
        print("✅ Scan job created successfully")
    except Exception as e:
        print(f"❌ Error creating scan job: {e}")
        return None
    
    print(f"\n✅ NEW SCAN JOB CREATED:")
    print(f"   - Scan ID: #{new_scan.id}")
    print(f"   - User: {new_scan.user.username}")
    print(f"   - Repository: {new_scan.repository.name}")
    print(f"   - SCM: {new_scan.repository.scm_profile.scm_type}")
    print(f"   - Branch: {new_scan.branch}")
    print(f"   - Status: {new_scan.status}")
    print(f"   - Triggered: {new_scan.triggered_at}")
    
    return new_scan.id

def check_system_status():
    """Check current system status"""
    from sast_report.models import ScanJob, VulnerabilityReport
    
    print("\n📊 SYSTEM STATUS:")
    total_scans = ScanJob.objects.count()
    queued = ScanJob.objects.filter(status='queued').count()
    in_progress = ScanJob.objects.filter(status='in_progress').count()
    completed = ScanJob.objects.filter(status='completed').count()
    
    print(f"   - Total scans: {total_scans}")
    print(f"   - Queued: {queued}")
    print(f"   - In Progress: {in_progress}")
    print(f"   - Completed: {completed}")
    print(f"   - Vulnerabilities: {VulnerabilityReport.objects.count()}")

if __name__ == '__main__':
    check_system_status()
    print("\n" + "=" * 50)
    scan_id = trigger_new_scan()
    
    if scan_id:
        print("\n" + "=" * 50)
        print(f"🎯 Scan #{scan_id} is now QUEUED and ready for processing!")
        print("💡 Keep the worker running to process this scan automatically.")
        
        # Show updated status
        from sast_report.models import ScanJob
        queued_now = ScanJob.objects.filter(status='queued').count()
        print(f"📈 Queued scans now: {queued_now}")
    else:
        print("\n❌ Failed to create scan job.")
