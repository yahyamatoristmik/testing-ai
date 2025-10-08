#!/usr/bin/env python3
import os
import sys
import django
import datetime

# Tambahkan path project ke Python path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Error setting up Django: {e}")
    sys.exit(1)

from sast_report.models import ScanJob
from django.utils import timezone

def fix_duration_data():
    """Fix existing duration data"""
    print("🔧 Fixing duration data...")
    
    scans = ScanJob.objects.all()
    fixed_count = 0
    error_count = 0
    
    for scan in scans:
        try:
            # Reset problematic duration
            if scan.scan_duration and not isinstance(scan.scan_duration, datetime.timedelta):
                print(f"⚠️ Fixing scan {scan.id} - invalid duration: {scan.scan_duration} (type: {type(scan.scan_duration)})")
                scan.scan_duration = None
                scan.save()
                fixed_count += 1
            
            # Recalculate if we have start/end times
            elif scan.finished_at and scan.started_at and not scan.scan_duration:
                print(f"🔄 Calculating duration for scan {scan.id}")
                scan.scan_duration = scan.finished_at - scan.started_at
                scan.save()
                fixed_count += 1
                
        except Exception as e:
            print(f"❌ Error fixing scan {scan.id}: {e}")
            error_count += 1
            continue
    
    print(f"✅ Fixed {fixed_count} scan records")
    print(f"❌ Errors: {error_count} scans")
    
    # Test the fix
    test_scan = ScanJob.objects.first()
    if test_scan:
        print(f"🧪 Test scan duration: {test_scan.scan_duration} (type: {type(test_scan.scan_duration)})")

if __name__ == "__main__":
    fix_duration_data()
