from django.core.management.base import BaseCommand
from django.utils import timezone
from sast_report.models import ScanJob
import datetime

class Command(BaseCommand):
    help = 'Fix duration data in ScanJob models'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--scan-id',
            type=int,
            help='Fix specific scan ID',
        )
    
    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing duration data...")
        
        scan_id = options.get('scan_id')
        
        if scan_id:
            scans = ScanJob.objects.filter(id=scan_id)
        else:
            scans = ScanJob.objects.all()
            
        fixed_count = 0
        error_count = 0
        
        for scan in scans:
            try:
                # Debug info
                self.stdout.write(f"📊 Scan {scan.id}: status={scan.status}, started={scan.started_at}, finished={scan.finished_at}")
                
                # Case 1: Reset semua duration ke NULL dulu
                self.stdout.write(f"🔄 Resetting duration for scan {scan.id}")
                scan.scan_duration = None
                
                # Case 2: Calculate duration untuk scan completed
                if scan.status == 'completed' and scan.started_at and scan.finished_at:
                    self.stdout.write(f"📐 Calculating duration for completed scan {scan.id}")
                    scan.scan_duration = scan.finished_at - scan.started_at
                
                scan.save()
                fixed_count += 1
                    
            except Exception as e:
                self.stdout.write(f"❌ Error fixing scan {scan.id}: {e}")
                error_count += 1
                continue
        
        self.stdout.write(f"✅ Fixed {fixed_count} scan records")
        
        if error_count > 0:
            self.stdout.write(f"❌ Errors: {error_count} scans")
        
        # Show final test
        test_scans = ScanJob.objects.all()[:3]
        self.stdout.write("🧪 Final test - First 3 scans:")
        for scan in test_scans:
            self.stdout.write(f"  Scan {scan.id}: duration={scan.scan_duration} (type: {type(scan.scan_duration)})")
