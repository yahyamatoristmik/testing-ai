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

from django.db import connection
from sast_report.models import ScanJob
import datetime

print("🚀 AGGRESSIVE FIX: Comprehensive duration fix...")

# Method 1: Reset SEMUA data duration dengan SQL langsung
with connection.cursor() as cursor:
    print("1. Aggressive reset semua duration...")
    cursor.execute("UPDATE sast_report_scanjob SET scan_duration = NULL")
    print(f"   ✅ Reset semua {cursor.rowcount} records")

# Method 2: Manual calculation untuk setiap completed scan
print("2. Manual calculation untuk completed scans...")
fixed_count = 0

# Gunasi raw SQL query untuk hindari Django ORM issues
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT id, started_at, finished_at 
        FROM sast_report_scanjob 
        WHERE status = 'completed' 
        AND started_at IS NOT NULL 
        AND finished_at IS NOT NULL
    """)
    completed_scans = cursor.fetchall()
    
    for scan_id, started_at, finished_at in completed_scans:
        try:
            # Calculate duration manually
            if started_at and finished_at:
                duration = finished_at - started_at
                # Update menggunakan SQL langsung
                cursor.execute(
                    "UPDATE sast_report_scanjob SET scan_duration = %s WHERE id = %s",
                    [duration, scan_id]
                )
                fixed_count += 1
                print(f"   ✅ Fixed scan {scan_id}: {duration}")
        except Exception as e:
            print(f"   ❌ Error fixing scan {scan_id}: {e}")

print(f"3. ✅ Fixed {fixed_count} completed scans")

# Method 3: Final verification dengan cara aman
print("4. Final verification...")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT id, status, scan_duration 
        FROM sast_report_scanjob 
        ORDER BY id 
        LIMIT 10
    """)
    scans = cursor.fetchall()
    
    print("   🧪 First 10 scans:")
    for scan_id, status, duration in scans:
        print(f"      Scan {scan_id} ({status}): duration={duration}")

print("✅ AGGRESSIVE FIX COMPLETED!")
