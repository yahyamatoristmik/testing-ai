import os
import sys
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport
from django.utils import timezone
from django.db import connection

def worker_fixed():
    print("🚀 FIXED SCAN WORKER STARTING")
    print("=" * 50)
    
    while True:
        try:
            # Find pending scans
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM sast_report_scanjob WHERE status = 'pending'")
                pending_ids = [row[0] for row in cursor.fetchall()]
            
            print(f"\n🔍 Found {len(pending_ids)} pending scans")
            
            for scan_id in pending_ids:
                try:
                    # Get scan info
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT s.id, r.name FROM sast_report_scanjob s JOIN sast_report_repository r ON s.repository_id = r.id WHERE s.id = %s",
                            [scan_id]
                        )
                        scan_data = cursor.fetchone()
                    
                    print(f"\n🔄 PROCESSING SCAN #{scan_data[0]}: {scan_data[1]}")
                    
                    # Update to running
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE sast_report_scanjob SET status = 'running', started_at = %s WHERE id = %s",
                            [timezone.now(), scan_id]
                        )
                    print("   ✅ Status: running")
                    
                    # Simulate work
                    time.sleep(2)
                    
                    # Create sample vulnerabilities
                    vulnerabilities = [
                        {
                            'rule_id': 'SQLI-001',
                            'severity': 'HIGH',
                            'confidence': 'HIGH',
                            'file_path': 'src/app.py',
                            'line_number': 45,
                            'message': 'SQL Injection found',
                            'description': 'User input in SQL query',
                            'recommendation': 'Use parameterized queries',
                            'code_snippet': 'query = "SELECT * FROM users"',
                            'cwe_id': 'CWE-89',
                            'owasp_category': 'A1: Injection'
                        }
                    ]
                    
                    # Create reports
                    for vuln in vulnerabilities:
                        VulnerabilityReport.objects.create(
                            scan_job_id=scan_id,
                            **vuln
                        )
                    
                    # Mark completed
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE sast_report_scanjob SET status = 'completed', finished_at = %s, findings_count = %s WHERE id = %s",
                            [timezone.now(), len(vulnerabilities), scan_id]
                        )
                    
                    print(f"🎉 Scan #{scan_id} COMPLETED!")
                    
                except Exception as e:
                  import os
import sys
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport
from django.utils import timezone
from django.db import connection

def worker_fixed():
    print("🚀 FIXED SCAN WORKER STARTING")
    print("=" * 50)
    
    while True:
        try:
            # Find pending scans
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM sast_report_scanjob WHERE status = 'pending'")
                pending_ids = [row[0] for row in cursor.fetchall()]
            
            print(f"\n🔍 Found {len(pending_ids)} pending scans")
            
            for scan_id in pending_ids:
                try:
                    # Get scan info
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT s.id, r.name FROM sast_report_scanjob s JOIN sast_report_repository r ON s.repository_id = r.id WHERE s.id = %s",
                            [scan_id]
                        )
                        scan_data = cursor.fetchone()
                    
                    print(f"\n🔄 PROCESSING SCAN #{scan_data[0]}: {scan_data[1]}")
                    
                    # Update to running
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE sast_report_scanjob SET status = 'running', started_at = %s WHERE id = %s",
                            [timezone.now(), scan_id]
                        )
                    print("   ✅ Status: running")
                    
                    # Simulate work
                    time.sleep(2)
                    
                    # Create sample vulnerabilities
                    vulnerabilities = [
                        {
                            'rule_id': 'SQLI-001',
                            'severity': 'HIGH',
                            'confidence': 'HIGH',
                            'file_path': 'src/app.py',
                            'line_number': 45,
                            'message': 'SQL Injection found',
                            'description': 'User input in SQL query',
                            'recommendation': 'Use parameterized queries',
                            'code_snippet': 'query = "SELECT * FROM users"',
                            'cwe_id': 'CWE-89',
                            'owasp_category': 'A1: Injection'
                        }
                    ]
                    
                    # Create reports
                    for vuln in vulnerabilities:
                        VulnerabilityReport.objects.create(
                            scan_job_id=scan_id,
                            **vuln
                        )
                    
                    # Mark completed
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE sast_report_scanjob SET status = 'completed', finished_at = %s, findings_count = %s WHERE id = %s",
                            [timezone.now(), len(vulnerabilities), scan_id]
                        )
                    
                    print(f"🎉 Scan #{scan_id} COMPLETED!")
                    
                except Exception as e:
                    print(f"❌ Error with scan #{scan_id}: {e}")
            
            # Status
            with connection.cursor() as cursor:
                cursor.execute("SELECT status, COUNT(*) FROM sast_report_scanjob GROUP BY status")
                for status, count in cursor.fetchall():
                    print(f"   {status}: {count}")
            
            time.sleep(10)
            
        except Exception as e:
            print(f"❌ Worker error: {e}")
            time.sleep(30)

if __name__ == '__main__':
    worker_fixed()  print(f"❌ Error with scan #{scan_id}: {e}")
            
            # Status
            with connection.cursor() as cursor:
                cursor.execute("SELECT status, COUNT(*) FROM sast_report_scanjob GROUP BY status")
                for status, count in cursor.fetchall():
                    print(f"   {status}: {count}")
            
            time.sleep(10)
            
        except Exception as e:
            print(f"❌ Worker error: {e}")
            time.sleep(30)

if __name__ == '__main__':
    worker_fixed()
