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
    
    # Initial status
    total_scans = ScanJob.objects.count()
    queued_scans = ScanJob.objects.filter(status='queued').count()
    completed_scans = ScanJob.objects.filter(status='completed').count()
    
    print(f"📊 Initial Status:")
    print(f"   - Total scans: {total_scans}")
    print(f"   - Queued: {queued_scans}")
    print(f"   - Completed: {completed_scans}")
    print("=" * 50)
    
    while True:
        try:
            # Find queued scans
            queued_scans = ScanJob.objects.filter(status='queued')
            print(f"\n🔍 Checking for queued scans... Found: {queued_scans.count()}")
            
            for scan in queued_scans:
                print(f"\n🔄 Processing Scan Job #{scan.id}")
                print(f"   Repository: {scan.repository_url}")
                print(f"   Target Branch: {scan.target_branch}")
                
                # Update status to in progress
                scan.status = 'in_progress'
                scan.started_at = timezone.now()
                scan.save()
                print("   ✅ Status updated to: in_progress")
                
                # Simulate scanning process with progress updates
                print("   📈 Scan progress:")
                steps = [
                    "Initializing scanner...",
                    "Fetching source code...", 
                    "Analyzing dependencies...",
                    "Running security checks...",
                    "Generating report..."
                ]
                
                for i, step in enumerate(steps, 1):
                    progress = (i / len(steps)) * 100
                    print(f"      [{progress:.0f}%] {step}")
                    time.sleep(2)  # Simulate work
                
                # Create sample vulnerability reports
                vulnerabilities = [
                    {
                        'title': 'SQL Injection Vulnerability',
                        'severity': 'high',
                        'description': 'Potential SQL injection in user input handling. User input is directly concatenated into SQL query.',
                        'file_path': 'src/auth/controllers.py',
                        'line_number': 45,
                        'code_snippet': 'query = f"SELECT * FROM users WHERE username = {user_input}"'
                    },
                    {
                        'title': 'Cross-Site Scripting (XSS)',
                        'severity': 'medium', 
                        'description': 'Unescaped user input in template rendering.',
                        'file_path': 'templates/user_profile.html',
                        'line_number': 23,
                        'code_snippet': '<div>Welcome {{ user_input }}</div>'
                    },
                    {
                        'title': 'Hardcoded API Key',
                        'severity': 'high',
                        'description': 'API key exposed in source code. Should use environment variables.',
                        'file_path': 'src/config/settings.py', 
                        'line_number': 12,
                        'code_snippet': 'API_KEY = "sk-1234567890abcdef"'
                    },
                    {
                        'title': 'Insecure Random Number Generator',
                        'severity': 'medium',
                        'description': 'Using predictable random number generator for security purposes.',
                        'file_path': 'src/utils/security.py',
                        'line_number': 8,
                        'code_snippet': 'token = random.randint(1000, 9999)'
                    }
                ]
                
                # Create vulnerability reports
                vuln_count = 0
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
                    print(f"   ✅ Found: {vuln_data['title']} ({vuln_data['severity']})")
                
                # Mark scan as completed
                scan.status = 'completed'
                scan.completed_at = timezone.now()
                scan.save()
                
                print(f"\n🎉 Scan Job #{scan.id} COMPLETED!")
                print(f"   📊 Vulnerabilities found: {vuln_count}")
                print(f"   ⏱️  Duration: {scan.completed_at - scan.started_at}")
                
                # Show vulnerability summary
                high_count = VulnerabilityReport.objects.filter(scan_job=scan, severity='high').count()
                medium_count = VulnerabilityReport.objects.filter(scan_job=scan, severity='medium').count()
                print(f"   📋 Summary - High: {high_count}, Medium: {medium_count}")
            
            # Show current status
            status_counts = {
                'queued': ScanJob.objects.filter(status='queued').count(),
                'in_progress': ScanJob.objects.filter(status='in_progress').count(),
                'completed': ScanJob.objects.filter(status='completed').count()
            }
            
            print(f"\n📈 Current System Status:")
            for status, count in status_counts.items():
                print(f"   - {status.upper()}: {count}")
            
            print(f"   - Total vulnerabilities: {VulnerabilityReport.objects.count()}")
            
            # Wait before next check
            print(f"\n⏰ Next check in 15 seconds...")
            print("=" * 50)
            time.sleep(15)
            
        except Exception as e:
            print(f"❌ Worker error: {e}")
            import traceback
            traceback.print_exc()
            print("🔄 Retrying in 30 seconds...")
            time.sleep(30)

if __name__ == '__main__':
    scan_worker()
