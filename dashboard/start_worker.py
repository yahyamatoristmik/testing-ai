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

from sast_report.models import ScanJob, VulnerabilityReport, Sast
from django.utils import timezone

def scan_worker():
    """Background worker to process scan jobs"""
    print("🚀 Starting Scan Worker...")
    print("📊 Initial scan jobs status:")
    
    while True:
        try:
            # Find queued scans
            queued_scans = ScanJob.objects.filter(status='queued')
            print(f"🔍 Checking for queued scans... Found: {queued_scans.count()}")
            
            for scan in queued_scans:
                print(f"\n🔄 Processing Scan Job #{scan.id}: {scan.repository_url}")
                
                # Update status to in progress
                scan.status = 'in_progress'
                scan.started_at = timezone.now()
                scan.save()
                print(f"   ✅ Status: in_progress")
                
                # Simulate scanning process (5 seconds)
                for i in range(1, 6):
                    print(f"   📈 Scanning... {i * 20}%")
                    time.sleep(1)
                
                # Create sample vulnerability reports
                vulnerabilities = [
                    {
                        'title': 'SQL Injection Vulnerability',
                        'severity': 'high',
                        'description': 'Potential SQL injection in user input handling',
                        'file_path': 'src/auth/controllers.py',
                        'line_number': 45
                    },
                    {
                        'title': 'Cross-Site Scripting (XSS)',
                        'severity': 'medium', 
                        'description': 'Unescaped user input in template',
                        'file_path': 'templates/user_profile.html',
                        'line_number': 23
                    },
                    {
                        'title': 'Hardcoded API Key',
                        'severity': 'high',
                        'description': 'API key exposed in source code',
                        'file_path': 'src/config/settings.py',
                        'line_number': 12
                    }
                ]
                
                # Create vulnerability reports
                for i, vuln_data in enumerate(vulnerabilities, 1):
                    vuln_report = VulnerabilityReport.objects.create(
                        scan_job=scan,
                        title=vuln_data['title'],
                        severity=vuln_data['severity'],
                        description=vuln_data['description'],
                        file_path=vuln_data['file_path'],
                        line_number=vuln_data['line_number'],
                        status='open'
                    )
                    print(f"   ✅ Created vulnerability: {vuln_data['title']} ({vuln_data['severity']})")
                
                # Mark scan as completed
                scan.status = 'completed'
                scan.completed_at = timezone.now()
                scan.save()
                
                print(f"🎉 Scan Job #{scan.id} COMPLETED!")
                print(f"   📊 Vulnerabilities found: {VulnerabilityReport.objects.filter(scan_job=scan).count()}")
            
            # Check for in-progress scans
            in_progress_scans = ScanJob.objects.filter(status='in_progress')
            if in_progress_scans.exists():
                print(f"\n⏳ Scans in progress: {in_progress_scans.count()}")
                for scan in in_progress_scans:
                    duration = timezone.now() - scan.started_at
                    print(f"   - Scan #{scan.id}: running for {duration.seconds}s")
            
            time.sleep(10)  # Check every 10 seconds
            
        except Exception as e:
            print(f"❌ Worker error: {e}")
            time.sleep(30)  # Wait longer if error

if __name__ == '__main__':
    scan_worker()
