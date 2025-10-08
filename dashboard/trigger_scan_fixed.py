import os
import sys
import django
from datetime import datetime

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob
from django.contrib.auth.models import User

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
    
    # Create new scan job with correct fields
    # First, let's see what fields are required by creating with minimal data
    try:
        new_scan = ScanJob.objects.create(
            user=user,
            status='queued'
            # Add other fields based on model inspection
        )
        print("✅ Scan job created with minimal fields")
    except Exception as e:
        print(f"❌ Error with minimal fields: {e}")
        # Try alternative approach
        return None
    
    print(f"✅ NEW SCAN JOB CREATED:")
    print(f"   - Scan ID: #{new_scan.id}")
    print(f"   - Status: {new_scan.status}")
    print(f"   - User: {new_scan.user.username}")
    print(f"   - Created: {new_scan.created_at}")
    
    # Try to update with additional data if fields exist
    try:
        if hasattr(new_scan, 'repository_url'):
            new_scan.repository_url = 'https://github.com/testuser/new-scan-repo.git'
        if hasattr(new_scan, 'target_branch'):
            new_scan.target_branch = 'main'
        if hasattr(new_scan, 'scan_type'):
            new_scan.scan_type = 'sast'
        
        new_scan.save()
        print("✅ Updated with additional scan details")
    except Exception as e:
        print(f"⚠️  Could not update additional fields: {e}")
    
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
        print("\n❌ Failed to create scan job. Check model structure.")
