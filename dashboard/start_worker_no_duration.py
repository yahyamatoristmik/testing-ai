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
    """Scan worker tanpa scan_duration untuk menghindari error"""
    print("🚀 STARTING WORKER (NO SCAN_DURATION)")
    print("=" * 60)
    
    while True:
        try:
            # Find queued scans
            queued_scans = ScanJob.objects.filter(status='queued')
            print(f"\n🔍 Checking for queued scans... Found: {queued_scans.count()}")
            
            for scan in queued_scans:
                print(f"\n🔄 PROCESSING SCAN #{scan.id}")
                print(f"   Repository: {scan.repository.name}")
                print(f"   Branch: {scan.branch}")
                
                # Update status to processing
                scan.status = 'processing'
                scan.started_at = timezone.now()
                scan.scan_duration = None  # Pastikan NULL
                scan.save()
                print("   ✅ Status: processing")
                
                # Simulate scanning
                print("   📈 Scanning in progress...")
                time.sleep(2)
                
                # Create vulnerabilities
                vulnerabilities = [
                    {
                        'rule_id': 'SQLI-001',
                        'severity': 'high',
                        'confidence': 'high', 
                        'file_path': 'src/auth/controller.py',
                        'line_number': 45,
                        'message': 'Potential SQL injection vulnerability',
                        'description': 'User input directly concatenated in SQL query',
                        'recommendation': 'Use parameterized queries',
                        'code_snippet': 'query = f"SELECT * FROM users WHERE username = {user_input}"',
                        'cwe_id': 'CWE-89',
                        'owasp_category': 'A1: Injection'
                    },
                    {
                        'rule_id': 'XSS-001',
                        'severity': 'medium',
                        'confidence': 'medium',
                        'file_path': 'templates/user/profile.html',
                        'line_number': 23,
                        'message': 'Potential XSS vulnerability',
                        'description': 'Unescaped user input in template',
                        'recommendation': 'Escape user inputs',
                        'code_snippet': '<div>Welcome {{ user_input }}</div>',
                        'cwe_id': 'CWE-79',
                        'owasp_category': 'A7: XSS'
                    }
                ]
                
                # Create vulnerability reports
                vuln_count = 0
                high_count = 0
                medium_count = 0
                
                for vuln_data in vulnerabilities:
                    VulnerabilityReport.objects.create(
                        scan_job=scan,
                        rule_id=vuln_data['rule_id'],
                        severity=vuln_data['severity'],
                        confidence=vuln_data['confidence'],
                        file_path=vuln_data['file_path'],
                        line_number=vuln_data['line_number'],
                        message=vuln_data['message'],
                        description=vuln_data['description'],
                        recommendation=vuln_data['recommendation'],
                        code_snippet=vuln_data['code_snippet'],
                        cwe_id=vuln_data['cwe_id'],
                        owasp_category=vuln_data['owasp_category'],
                        is_false_positive=False
                    )
                    vuln_count += 1
                    
                    if vuln_data['severity'] == 'high':
                        high_count += 1
                    elif vuln_data['severity'] == 'medium':
                        medium_count += 1
                    
                    print(f"   ✅ {vuln_data['rule_id']}: {vuln_data['message']}")
                
                # Mark as completed - TANPA scan_duration
                scan.status = 'completed'  # Gunakan 'completed' bukan 'done' untuk konsistensi
                scan.finished_at = timezone.now()
                scan.findings_count = vuln_count
                scan.high_count = high_count
                scan.medium_count = medium_count
                scan.scan_duration = None  # Tetap NULL
                
                scan.save()
                
                print(f"\n🎉 SCAN #{scan.id} COMPLETED SUCCESSFULLY!")
                print(f"   📊 Findings: {vuln_count}")
                print(f"   📋 High: {high_count}, Medium: {medium_count}")
                print(f"   ⏱️  Actual duration: {scan.finished_at - scan.started_at}")
            
            # Status report
            print(f"\n📈 SYSTEM STATUS:")
            print(f"   - Queued: {ScanJob.objects.filter(status='queued').count()}")
            print(f"   - Processing: {ScanJob.objects.filter(status='processing').count()}")
            print(f"   - Completed: {ScanJob.objects.filter(status='completed').count()}")
            print(f"   - Total Vulnerabilities: {VulnerabilityReport.objects.count()}")
            
            # Wait
            if queued_scans.count() == 0:
                print(f"\n⏰ No queued scans. Waiting 10 seconds...")
                time.sleep(10)
            
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Worker error: {e}")
            import traceback
            traceback.print_exc()
            print("🔄 Retrying in 30 seconds...")
            time.sleep(30)

if __name__ == '__main__':
    scan_worker()
