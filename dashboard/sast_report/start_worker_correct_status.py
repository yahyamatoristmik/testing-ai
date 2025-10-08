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
from django.db import connection

def scan_worker_correct():
    """Worker dengan status yang sesuai model"""
    print("🚀 SCAN WORKER WITH CORRECT STATUS")
    print("=" * 60)
    
    while True:
        try:
            # Find queued/pending scans
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM sast_report_scanjob WHERE status IN ('queued', 'pending')")
                queued_scan_ids = [row[0] for row in cursor.fetchall()]
            
            print(f"\n🔍 Checking for scans... Found: {len(queued_scan_ids)}")
            
            for scan_id in queued_scan_ids:
                try:
                    # Get scan info
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT s.id, r.name, s.branch FROM sast_report_scanjob s JOIN sast_report_repository r ON s.repository_id = r.id WHERE s.id = %s",
                            [scan_id]
                        )
                        scan_data = cursor.fetchone()
                    
                    print(f"\n🔄 PROCESSING SCAN #{scan_data[0]}")
                    print(f"   Repository: {scan_data[1]}")
                    print(f"   Branch: {scan_data[2]}")
                    
                    # Update status to running (sesuai model)
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE sast_report_scanjob SET status = 'running', started_at = %s WHERE id = %s",
                            [timezone.now(), scan_id]
                        )
                    print("   ✅ Status: running")
                    
                    # Simulate scanning
                    print("   📈 Scanning in progress...")
                    time.sleep(3)
                    
                    # Create sample vulnerabilities
                    vulnerabilities = [
                        {
                            'rule_id': 'SQLI-001',
                            'severity': 'HIGH',
                            'confidence': 'HIGH', 
                            'file_path': 'src/auth/controller.py',
                            'line_number': 45,
                            'message': 'SQL Injection vulnerability detected',
                            'description': 'User input directly concatenated in SQL query without parameterization',
                            'recommendation': 'Use parameterized queries or prepared statements',
                            'code_snippet': 'query = f"SELECT * FROM users WHERE username = {user_input}"',
                            'cwe_id': 'CWE-89',
                            'owasp_category': 'A1: Injection'
                        },
                        {
                            'rule_id': 'XSS-001',
                            'severity': 'MEDIUM',
                            'confidence': 'MEDIUM',
                            'file_path': 'templates/user/profile.html', 
                            'line_number': 23,
                            'message': 'Cross-site scripting vulnerability',
                            'description': 'Unescaped user input in template rendering',
                            'recommendation': 'Escape all user inputs before rendering in templates',
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
                            scan_job_id=scan_id,
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
                        
                        if vuln_data['severity'] == 'HIGH':
                            high_count += 1
                        elif vuln_data['severity'] == 'MEDIUM':
                            medium_count += 1
                        
                        print(f"   ✅ {vuln_data['rule_id']}: {vuln_data['message']}")
                    
                    # Mark as completed (sesuai model)
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE sast_report_scanjob SET status = 'completed', finished_at = %s, findings_count = %s, high_count = %s, medium_count = %s WHERE id = %s",
                            [timezone.now(), vuln_count, high_count, medium_count, scan_id]
                        )
                    
                    print(f"\n🎉 SCAN #{scan_id} COMPLETED!")
                    print(f"   📊 Findings: {vuln_count}")
                    print(f"   📋 High: {high_count}, Medium: {medium_count}")
                    
                except Exception as e:
                    print(f"❌ Error processing scan #{scan_id}: {e}")
                    # Mark as failed
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE sast_report_scanjob SET status = 'failed' WHERE id = %s",
                            [scan_id]
                        )
            
            # Status report
            with connection.cursor() as cursor:
                cursor.execute("SELECT status, COUNT(*) FROM sast_report_scanjob GROUP BY status")
                status_data = cursor.fetchall()
            
            print(f"\n📈 SYSTEM STATUS:")
            for status, count in status_data:
                print(f"   - {status.upper()}: {count}")
            
            total_vulns = VulnerabilityReport.objects.count()
            print(f"   - Total Vulnerabilities: {total_vulns}")
            
            # Wait
            if len(queued_scan_ids) == 0:
                print(f"\n⏰ No queued scans. Waiting 10 seconds...")
                time.sleep(10)
            
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Worker error: {e}")
            print("🔄 Retrying in 30 seconds...")
            time.sleep(30)

if __name__ == '__main__':
    scan_worker_correct()
