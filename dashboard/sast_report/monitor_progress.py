import os
import sys
import django
import time

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport

def monitor_progress():
    print("📡 LIVE PROGRESS MONITOR")
    print("=" * 50)
    
    previous_queued = -1
    previous_completed = -1
    
    try:
        while True:
            # Get current status
            queued = ScanJob.objects.filter(status='queued').count()
            in_progress = ScanJob.objects.filter(status='in_progress').count()
            completed = ScanJob.objects.filter(status='completed').count()
            total_vulns = VulnerabilityReport.objects.count()
            
            # Only print if something changed
            if (queued != previous_queued or completed != previous_completed):
                print(f"\n🕒 {time.strftime('%H:%M:%S')}")
                print(f"   📊 Queued: {queued} | In Progress: {in_progress} | Completed: {completed}")
                print(f"   ⚠️  Vulnerabilities: {total_vulns}")
                
                # Show details of in-progress scans
                if in_progress > 0:
                    print("   🔄 Currently processing:")
                    for scan in ScanJob.objects.filter(status='in_progress'):
                        duration = timezone.now() - scan.started_at
                        print(f"      - Scan #{scan.id}: {duration.seconds}s")
                
                previous_queued = queued
                previous_completed = completed
            
            time.sleep(5)  # Update every 5 seconds
            
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring stopped")

if __name__ == '__main__':
    monitor_progress()
