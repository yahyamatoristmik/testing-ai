import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.db import connection

def fix_existing_scans():
    print("🔧 FIXING EXISTING SCANS STATUS")
    print("=" * 50)
    
    # Update status yang tidak sesuai
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
            print(f"✅ Updated {old_status} -> {new_status}")
    
    print("\n🎯 ALL SCAN STATUSES FIXED!")

if __name__ == '__main__':
    fix_existing_scans()
