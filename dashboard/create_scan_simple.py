import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob
from django.contrib.auth.models import User

def create_minimal_scan():
    """Create scan with absolute minimum required fields"""
    print("🎯 CREATING MINIMAL SCAN JOB")
    print("=" * 40)
    
    # Get user
    user = User.objects.first()
    if not user:
        user = User.objects.create_user('minimal_user', 'min@test.com', 'pass123')
        print("✅ Created minimal user")
    
    # Create scan with only required fields
    try:
        scan = ScanJob.objects.create(
            user=user,
            status='queued'
        )
        print(f"✅ SUCCESS: Scan #{scan.id} created")
        print(f"   User: {scan.user.username}")
        print(f"   Status: {scan.status}")
        print(f"   ID: {scan.id}")
        
        # Show all fields of the created scan
        print(f"\n📋 SCAN FIELDS:")
        for field in ScanJob._meta.get_fields():
            if not field.is_relation and not field.auto_created:
                try:
                    value = getattr(scan, field.name)
                    if value is not None:  # Only show non-null values
                        print(f"   - {field.name}: {value}")
                except:
                    pass
                    
        return scan.id
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return None

if __name__ == '__main__':
    create_minimal_scan()
