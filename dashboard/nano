import os
import sys
import django
from datetime import datetime

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, Repository
from django.contrib.auth.models import User

def create_or_get_repository():
    """Create or get a test repository"""
    try:
        # Try to get existing test repository
        repo = Repository.objects.get(name='Test Repository')
        print("✅ Using existing test repository")
        return repo
    except Repository.DoesNotExist:
        try:
            # Create new repository
            repo = Repository.objects.create(
                name='Test Repository',
                url='https://github.com/testuser/test-repo.git',
                description='Test repository for SAST scanning',
                is_active=True
            )
            print("✅ Created new test repository")
            return repo
        except Exception as e:
            print(f"❌ Failed to create repository: {e}")
            return None

def trigger_new_scan():
    print("🚀 TRIGGERING NEW SCAN JOB")
    print("=" * 50)
    
    # Get or create test user
    try:
        user = User.objects.get(username='sast_test_user')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='sast_test_user',
            email='test@example.com',
            password='testpass123'
        )
        print("✅ Created test user")
    
    # Get or create repository
    repository = create_or_get_repository()
    if not repository:
        print("❌ Cannot proceed without repository")
        return None
    
    # Create new scan job with required repository
    try:
        new_scan = ScanJob.objects.create(
            user=user,
            repository=repository,
            branch='main',
            status='queued',
            triggered_at=datetime.now()
        )
        print("✅ Scan job created successfully")
    except Exception as e:
        print(f"❌ Error creating scan job: {e}")
        return None
    
    print(f"✅ NEW SCAN JOB CREATED:")
    print(f"   - Scan ID: #{new_scan.id}")
    print(f"   - Repository: {new_scan.repository.name}")
    print(f"   - Branch: {new_scan.branch}")
    print(f"   - Status: {new_scan.status}")
    print(f"   - Triggered: {new_scan.triggered_at}")
    print(f"   - User: {new_scan.user.username}")
    
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
    else:
        print("\n❌ Failed to create scan job.")
