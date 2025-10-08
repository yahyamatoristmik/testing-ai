import os
import sys
import django
import time
from datetime import datetime

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport
from django.utils import timezone

def scan_worker():
    """Background worker to process scan jobs"""
    print("🚀 Starting Scan Worker (Fixed Status)...")
    print("=" * 50)
    
    while True:
        try:
            # Find queued scans - use status values that fit in the column
            queued_scans = ScanJob.objects.filter(status='queued')
            print(f"\n🔍 Checking for queued scans... Found: {queued_scans.count()}")
            
            for scan in queued_scans:
                print(f"\n🔄 Processing Scan Job #{scan.id}")
                print(f"   Repository: {scan.repository.name}")
                print(f"   Branch: {scan.branch}")
                print(f"   User: {scan.user.username}")
                
                # Update status to processing (shorter value)
                scan.status = 'processing'  # Use shorter status
                scan.started_at = timezone.now()
                scan.save()
                print("   ✅ Status updated to: processing")
                
                # Simulate scanning process
                print("   📈 Scan progress:")
                steps = [
                    "Initializing...",
                    "Fetching code...", 
                    "Analyzing...",
                    "Security checks...",
                    "Generating report..."
                ]
                
                for i, step in enumerate(steps, 1):
                    progress = (i / len(steps)) * 100
                    print(f"      [{progress:.0f}%] {step}")
                    time.sleep(1)
                
                # Create sample vulnerability reports
                vulnerabilities = [
                    {
                        'title': 'SQL Injection Found',
                        'severity': 'high',
                        'description': 'User input directly in SQL query',
                        'file_path': 'src/auth/controller.py',
                        'line_number': 45,
                    },
                    {
                        'title': 'XSS in Template',
                        'severity': 'medium', 
                        'description': 'Unescaped user input',
                        'file_path': 'templates/profile.html',
                        'line_number': 23,
                    },
                    {
                        'title': 'Hardcoded API Key',
                        'severity': 'high',
                        'description': 'API key in config file',
                        'file_path': 'config/settings.py', 
                        'line_number': 12,
                    }
                ]
                
                # Create vulnerability reports
                vuln_count = 0
                high_count = 0
                medium_count = 0
                
                for vuln_data in vulnerabilities:
                    vuln_report = VulnerabilityReport.objects.create(
                        scan_job=scan,
                        title=vuln_data['title'],
                        severity=vuln_data['severity'],
                        description=vuln_data['description'],
                        file_path=vuln_data['file_path'],
                        line_number=vuln_data['line_number'],
                        status='open'
                    )
                    vuln_count += 1
                    
                    if vuln_data['severity'] == 'high':
                        high_count += 1
                    elif vuln_data['severity'] == 'medium':
                        medium_count += 1
                    
                    print(f"   ✅ Found: {vuln_data['title']} ({vuln_data['severity']})")
                
                # Mark scan as completed
                scan.status = 'done'  # Use shorter status
                scan.finished_at = timezone.now()
                scan.findings_count = vuln_count
                scan.high_count = high_count
                scan.medium_count = medium_count
                
                if scan.started_at:
                    scan.scan_duration = scan.finished_at - scan.started_at
                
                scan.save()
                
                print(f"\n🎉 Scan Job #{scan.id} COMPLETED!")
                print(f"   📊 Findings: {vuln_count}")
                print(f"   📋 High: {high_count}, Medium: {medium_count}")
            
            # Show current status
            status_counts = {
                'queued': ScanJob.objects.filter(status='queued').count(),
                'processing': ScanJob.objects.filter(status='processing').count(),
                'done': ScanJob.objects.filter(status='done').count()
            }
            
            print(f"\n📈 Current System Status:")
            for status, count in status_counts.items():
                print(f"   - {status.upper()}: {count}")
            
            total_vulns = VulnerabilityReport.objects.count()
            print(f"   - Total vulnerabilities: {total_vulns}")
            
            # Wait before next check
            if queued_scans.count() == 0:
                print(f"\n⏰ No queued scans. Next check in 10 seconds...")
                time.sleep(10)
            
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Worker error: {e}")
            import traceback
            traceback.print_exc()
            print("🔄 Retrying in 30 seconds...")
            time.sleep(30)

if __name__ == '__main__':
    scan_worker()
