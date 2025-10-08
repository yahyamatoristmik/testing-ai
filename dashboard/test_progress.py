import os
import django
import time
from django.test import Client
from django.contrib.auth import get_user_model
from sast_report.models import ScanJob, Vulnerability

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

def simulate_scan_progress():
    print("🔧 SIMULATING SCAN PROGRESS")
    print("==================================================")
    
    # Get the latest scan job
    latest_scan = ScanJob.objects.order_by('-id').first()
    if not latest_scan:
        print("❌ No scan jobs found")
        return
    
    print(f"📋 Scan Job #{latest_scan.id}: {latest_scan.repository_url}")
    print(f"🕒 Initial Status: {latest_scan.status}")
    
    # Simulate progress
    status_flow = ['queued', 'in_progress', 'completed']
    for status in status_flow:
        latest_scan.status = status
        latest_scan.save()
        print(f"   ✅ Status updated to: {status}")
        time.sleep(2)  # Simulate processing time
    
    # Add real-time progress updates
    print("\n📊 SIMULATING REAL-TIME PROGRESS:")
    for i in range(1, 101, 20):
        print(f"   📈 Progress: {i}%")
        time.sleep(1)
    
    print(f"\n🎉 Scan Job #{latest_scan.id} COMPLETED!")
    print(f"   📊 Total vulnerabilities: {Vulnerability.objects.filter(scan_job=latest_scan).count()}")

if __name__ == '__main__':
    simulate_scan_progress()
