import os
import sys
import django

# Setup Django - dari root directory
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.db import connection

def fix_all_issues():
    print("🔧 FIXING ALL SCAN ISSUES")
    print("=" * 50)
    
    # 1. Fix scan statuses
    print("1. 🔄 UPDATING SCAN STATUSES...")
    status_updates = [
        ('processing', 'running'),
        ('done', 'completed'), 
        ('queued', 'pending')
    ]
    
    for old_status, new_status in status_updates:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE sast_report_scanjob SET status = %s WHERE status = %s",
                [new_status, old_status]
            )
            print(f"   ✅ {old_status} -> {new_status}")
    
    # 2. Set scan_duration to NULL untuk hindari error
    print("\n2. 🗑️  CLEARING SCAN_DURATION...")
    with connection.cursor() as cursor:
        cursor.execute("UPDATE sast_report_scanjob SET scan_duration = NULL")
        print("   ✅ All scan_duration set to NULL")
    
    # 3. Create test scan jika tidak ada yang pending
    print("\n3. 🎯 CHECKING FOR PENDING SCANS...")
    from sast_report.models import ScanJob, Repository
    from django.contrib.auth.models import User
    
    pending_scans = ScanJob.objects.filter(status='pending').count()
    print(f"   Pending scans: {pending_scans}")
    
    if pending_scans == 0:
        user = User.objects.first()
        repository = Repository.objects.first()
        if user and repository:
            scan = ScanJob.objects.create(
                user=user,
                repository=repository,
                branch='main',
                status='pending',
                findings_count=0
            )
            print(f"   ✅ Created test scan #{scan.id}")
    
    print("\n🎯 ALL FIXES APPLIED!")

if __name__ == '__main__':
    fix_all_issues()
