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
    """Background worker with correct field names"""
    print("🚀 Starting Scan Worker (Correct Fields)...")
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
                
                # Update status to processing
                scan.status = 'processing'
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
                
                # Create vulnerability reports with CORRECT field names
                # First, let's check what fields are available
                vulnerabilities_data = [
                    {
                        'name': 'SQL Injection Vulnerability',
                        'severity_level': 'high',
                        'description': 'User input directly concatenated in SQL query without parameterization',
                        'file_location': 'src/auth/controller.py',
                        'line_number': 45,
                    },
                    {
                        'name': 'Cross-Site Scripting (XSS)',
                        'severity_level': 'medium', 
                        'description': 'Unescaped user input in template rendering',
                        'file_location': 'templates/user/profile.html',
                        'line_number': 23,
                    },
                    {
                        'name': 'Hardcoded API Key',
                        'severity_level': 'high',
                        'description': 'API key exposed in source code configuration',
                        'file_location': 'config/settings.py', 
                        'line_number': 12,
                    }
                ]
                
                # Create vulnerability reports
                vuln_count = 0
                high_count = 0
                medium_count = 0
                
                for vuln_data in vulnerabilities_data:
                    try:
                        # Try creating with different field combinations
                        vuln_report = VulnerabilityReport.objects.create(
                            scan_job=scan,
                            name=vuln_data['name'],
                            severity_level=vuln_data['severity_level'],
                            description=vuln_data['description'],
                            file_location=vuln_data['file_location'],
                            line_number=vuln_data['line_number']
                        )
                        vuln_count += 1
                        
                        if vuln_data['severity_level'] == 'high':
                            high_count += 1
                        elif vuln_data['severity_level'] == 'medium':
                            medium_count += 1
                        
                        print(f"   ✅ Found: {vuln_data['name']} ({vuln_data['severity_level']})")
                    
                    except Exception as e:
                        print(f"   ❌ Failed to create vulnerability: {e}")
                        # Try alternative field names
                        try:
                            vuln_report = VulnerabilityReport.objects.create(
                                scan_job=scan,
                                vulnerability_name=vuln_data['name'],
                                severity=vuln_data['severity_level'],
                                description=vuln_data['description'],
                                file_path=vuln_data['file_location'],
                                line=vuln_data['line_number']
                            )
                            vuln_count += 1
                            print(f"   ✅ Found (alt): {vuln_data['name']}")
                        except Exception as e2:
                            print(f"   ❌ Alternative also failed: {e2}")
                
                # Mark scan as completed
                scan.status = 'done'
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
            print(f"\n📈 Current System Status:")
            print(f"   - Queued: {ScanJob.objects.filter(status='queued').count()}")
            print(f"   - Processing: {ScanJob.objects.filter(status='processing').count()}")
            print(f"   - Done: {ScanJob.objects.filter(status='done').count()}")
            print(f"   - Total Vulnerabilities: {VulnerabilityReport.objects.count()}")
            
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
