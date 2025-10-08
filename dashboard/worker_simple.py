import os
import sys
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport
from django.utils import timezone
from django.db import connection

def simple_worker():
    print("🚀 SIMPLE WORKER STARTING")
    print("=" * 50)
    
    while True:
        try:
            # Process pending scans
            pending_scans = ScanJob.objects.filter(status='pending')
            print(f"🔍 Found {pending_scans.count()} pending scans")
            
            for scan in pending_scans:
                print(f"\n🔄 PROCESSING SCAN #{scan.id}: {scan.repository.name}")
                
                # Update to running
                scan.status = 'running'
                scan.started_at = timezone.now()
                scan.save()
                
                # Simulate work
                time.sleep(2)
                
                # Create sample vulnerability
                VulnerabilityReport.objects.create(
                    scan_job=scan,
                    rule_id='TEST-001',
                    severity='HIGH',
                    confidence='HIGH',
                    file_path='src/test.py',
                    line_number=1,
                    message='Test vulnerability',
                    description='This is a test vulnerability',
                    recommendation='Fix this issue',
                    code_snippet='print("test")',
                    cwe_id='CWE-000',
                    owasp_category='TEST'
                )
                
                # Mark completed
                scan.status = 'completed'
                scan.finished_at = timezone.now()
                scan.findings_count = 1
                scan.high_count = 1
                scan.save()
                
                print(f"🎉 Scan #{scan.id} COMPLETED with 1 finding")
            
            # Status
            status_counts = ScanJob.objects.values('status').annotate(count=Count('id'))
            print(f"\n📊 Current status: {list(status_counts)}")
            
            time.sleep(10)
            
        except Exception as e:
            print(f"❌ Worker error: {e}")
            time.sleep(30)

if __name__ == '__main__':
    simple_worker()
