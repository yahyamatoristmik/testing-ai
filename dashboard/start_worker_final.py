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
    print("🚀 Starting Scan Worker...")
    print("=" * 50)
    
    while True:
        try:
            # Find queued scans
            queued_scans = ScanJob.objects.filter(status='queued')
            print(f"\n🔍 Checking for queued scans... Found: {queued_scans.count()}")
            
            for scan in queued_scans:
                print(f"\n🔄 Processing Scan Job #{scan.id}")
                print(f"   Repository: {scan.repository.name}")
                print(f"   Branch: {scan.branch}")
                print(f"   User: {scan.user.username}")
                print(f"   SCM: {scan.repository.scm_profile.scm_type}")
                
                # Update status to in progress
                scan.status = 'in_progress'
                scan.started_at = timezone.now()
                scan.save()
                print("   ✅ Status updated to: in_progress")
                
                # Simulate scanning process
                print("   📈 Scan progress:")
                steps = [
                    ("Initializing scanner...", 10),
                    ("Fetching source code...", 20), 
                    ("Analyzing dependencies...", 40),
                    ("Running security checks...", 70),
                    ("Generating report...", 90),
                    ("Finalizing...", 100)
                ]
                
                for step, progress in steps:
                    print(f"      [{progress}%] {step}")
                    time.sleep(1)  # Shorter delay for testing
                
                # Create sample vulnerability reports
                vulnerabilities = [
                    {
                        'title': 'SQL Injection in UserController',
                        'severity': 'high',
                        'description': 'User input directly used in SQL query without parameterization',
                        'file_path': 'src/controllers/UserController.py',
                        'line_number': 45,
                    },
                    {
                        'title': 'XSS in Profile Template',
                        'severity': 'medium', 
                        'description': 'Unescaped user input in profile template',
                        'file_path': 'templates/user/profile.html',
                        'line_number': 23,
                    },
                    {
                        'title': 'Hardcoded Database Password',
                        'severity': 'high',
                        'description': 'Database password exposed in configuration file',
                        'file_path': 'config/database.py', 
                        'line_number': 12,
                    },
                    {
                        'title': 'Insecure Deserialization',
                        'severity': 'medium',
                        'description': 'User input deserialized without validation',
                        'file_path': 'src/utils/serializers.py',
                        'line_number': 67,
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
                    
                    # Count by severity
                    if vuln_data['severity'] == 'high':
                        high_count += 1
                    elif vuln_data['severity'] == 'medium':
                        medium_count += 1
                    
                    print(f"   ✅ Found: {vuln_data['title']} ({vuln_data['severity']})")
                
                # Mark scan as completed with statistics
                scan.status = 'completed'
                scan.finished_at = timezone.now()
                scan.findings_count = vuln_count
                scan.high_count = high_count
                scan.medium_count = medium_count
                
                # Calculate duration
                if scan.started_at:
                    scan.scan_duration = scan.finished_at - scan.started_at
                
                scan.save()
                
                print(f"\n🎉 Scan Job #{scan.id} COMPLETED!")
                print(f"   📊 Total findings: {vuln_count}")
                print(f"   📋 Severity breakdown:")
                print(f"      - High: {high_count}")
                print(f"      - Medium: {medium_count}")
                if scan.scan_duration:
                    print(f"   ⏱️  Duration: {scan.scan_duration}")
            
            # Show current status
            status_counts = {
                'queued': ScanJob.objects.filter(status='queued').count(),
                'in_progress': ScanJob.objects.filter(status='in_progress').count(),
                'completed': ScanJob.objects.filter(status='completed').count()
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
            else:
                time.sleep(5)
            
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Worker error: {e}")
            import traceback
            traceback.print_exc()
            print("🔄 Retrying in 30 seconds...")
            time.sleep(30)

if __name__ == '__main__':
    scan_worker()
