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

print("🚀 EMERGENCY SQL FIX: Fixing duration data with direct SQL...")

# Method 1: Reset semua duration ke NULL
with connection.cursor() as cursor:
    print("1. Resetting all durations to NULL...")
    cursor.execute("UPDATE sast_report_scanjob SET scan_duration = NULL")
    print(f"   ✅ Reset {cursor.rowcount} records")

# Method 2: Calculate duration untuk completed scans menggunakan SQL
with connection.cursor() as cursor:
    print("2. Calculating durations for completed scans...")
    cursor.execute("""
        UPDATE sast_report_scanjob 
        SET scan_duration = (finished_at - started_at)
        WHERE status = 'completed' 
        AND started_at IS NOT NULL 
        AND finished_at IS NOT NULL
    """)
    print(f"   ✅ Updated {cursor.rowcount} completed scans")

# Method 3: Verify fix
with connection.cursor() as cursor:
    print("3. Verifying fix...")
    cursor.execute("""
        SELECT id, status, started_at, finished_at, scan_duration 
        FROM sast_report_scanjob 
        LIMIT 5
    """)
    rows = cursor.fetchall()
    print("   🧪 First 5 scans after fix:")
    for row in rows:
        print(f"      Scan {row[0]}: {row[1]}, duration={row[4]}")

print("✅ EMERGENCY FIX COMPLETED!")
