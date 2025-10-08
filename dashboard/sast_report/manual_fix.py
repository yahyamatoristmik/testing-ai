#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
sys.path.append('/home/dj/ai-evaluator/dashboard')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

from sast_report.models import ScanJob
from django.db import connection
import datetime

print("🚀 MANUAL FIX: Fixing duration data...")

# Method 1: Reset semua duration problematic
scans = ScanJob.objects.all()
fixed_count = 0

for scan in scans:
    try:
        # Debug info
        print(f"Scan {scan.id}: status={scan.status}, started={scan.started_at}, finished={scan.finished_at}, duration={scan.scan_duration}")
        
        # Reset jika duration bukan timedelta
        if scan.scan_duration and not isinstance(scan.scan_duration, datetime.timedelta):
            print(f"⚠️ Resetting invalid duration for scan {scan.id}")
            scan.scan_duration = None
            scan.save()
            fixed_count += 1
        
        # Calculate duration untuk scan completed
        elif scan.status == 'completed' and scan.started_at and scan.finished_at and not scan.scan_duration:
            print(f"🔄 Calculating duration for scan {scan.id}")
            scan.scan_duration = scan.finished_at - scan.started_at
            scan.save()
            fixed_count += 1
            
    except Exception as e:
        print(f"❌ Error with scan {scan.id}: {e}")
        continue

print(f"✅ Fixed {fixed_count} scan records")

# Test final result
test_scans = ScanJob.objects.all()[:5]
print("🧪 Final test - First 5 scans:")
for scan in test_scans:
    print(f"  Scan {scan.id}: duration={scan.scan_duration} (type: {type(scan.scan_duration)})")
