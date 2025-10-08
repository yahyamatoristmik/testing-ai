# sast_report/management/commands/fix_corrupt_data.py
from django.core.management.base import BaseCommand
from django.db import connection
from sast_report.models import ScanJob
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Completely fix all corrupt duration data in database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force fix all duration data (even if not obviously corrupt)',
        )
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 STARTING COMPLETE DATA FIX...')
        self.stdout.write('=' * 50)
        
        total_fixed = 0
        
        # STEP 1: Analyze corrupt data
        self.stdout.write('📊 STEP 1: Analyzing corrupt data...')
        corrupt_data = self.analyze_corrupt_data()
        
        # STEP 2: Fix via direct SQL (most effective)
        self.stdout.write('🔧 STEP 2: Fixing via direct SQL...')
        sql_fixed = self.fix_via_sql()
        total_fixed += sql_fixed
        
        # STEP 3: Fix via Django ORM
        self.stdout.write('🛠️ STEP 3: Fixing via Django ORM...')
        orm_fixed = self.fix_via_orm(options['force'])
        total_fixed += orm_fixed
        
        # STEP 4: Verify fix
        self.stdout.write('✅ STEP 4: Verifying fix...')
        remaining_corrupt = self.verify_fix()
        
        # FINAL REPORT
        self.stdout.write('=' * 50)
        self.stdout.write('📋 FINAL REPORT:')
        self.stdout.write(f'   • SQL Fixed: {sql_fixed} records')
        self.stdout.write(f'   • ORM Fixed: {orm_fixed} records')
        self.stdout.write(f'   • Total Fixed: {total_fixed} records')
        self.stdout.write(f'   • Remaining Corrupt: {remaining_corrupt} records')
        
        if remaining_corrupt == 0:
            self.stdout.write(self.style.SUCCESS('🎉 ALL CORRUPT DATA FIXED SUCCESSFULLY!'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ {remaining_corrupt} records still need attention'))
    
    def analyze_corrupt_data(self):
        """Analyze what kind of corrupt data exists"""
        self.stdout.write('   🔍 Analyzing database...')
        
        with connection.cursor() as cursor:
            # Check total records
            cursor.execute("SELECT COUNT(*) FROM sast_report_scanjob")
            total_records = cursor.fetchone()[0]
            
            # Check records with duration
            cursor.execute("SELECT COUNT(*) FROM sast_report_scanjob WHERE scan_duration IS NOT NULL")
            records_with_duration = cursor.fetchone()[0]
            
            # Check obviously corrupt records (not containing 'days')
            cursor.execute("""
                SELECT COUNT(*) FROM sast_report_scanjob 
                WHERE scan_duration IS NOT NULL 
                AND scan_duration NOT LIKE '%%days%%'
            """)
            obviously_corrupt = cursor.fetchone()[0]
            
            # Check NULL durations
            cursor.execute("SELECT COUNT(*) FROM sast_report_scanjob WHERE scan_duration IS NULL")
            null_durations = cursor.fetchone()[0]
        
        self.stdout.write(f'   • Total Records: {total_records}')
        self.stdout.write(f'   • Records with Duration: {records_with_duration}')
        self.stdout.write(f'   • Obviously Corrupt: {obviously_corrupt}')
        self.stdout.write(f'   • NULL Durations: {null_durations}')
        
        return {
            'total': total_records,
            'with_duration': records_with_duration,
            'corrupt': obviously_corrupt,
            'null': null_durations
        }
    
    def fix_via_sql(self):
        """Fix corrupt data using direct SQL (most effective)"""
        self.stdout.write('   🗄️ Running SQL fixes...')
        
        try:
            with connection.cursor() as cursor:
                # Fix 1: Clear obviously corrupt data (not containing 'days')
                cursor.execute("""
                    UPDATE sast_report_scanjob 
                    SET scan_duration = NULL 
                    WHERE scan_duration IS NOT NULL 
                    AND scan_duration NOT LIKE '%%days%%'
                """)
                fix1_count = cursor.rowcount
                
                # Fix 2: Clear any duration for pending/failed scans (they shouldn't have duration)
                cursor.execute("""
                    UPDATE sast_report_scanjob 
                    SET scan_duration = NULL 
                    WHERE status IN ('pending', 'failed', 'cancelled')
                    AND scan_duration IS NOT NULL
                """)
                fix2_count = cursor.rowcount
                
                total_fixed = fix1_count + fix2_count
                
                self.stdout.write(f'   • Fixed obviously corrupt: {fix1_count}')
                self.stdout.write(f'   • Fixed invalid status durations: {fix2_count}')
                
                return total_fixed
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ SQL fix failed: {e}'))
            return 0
    
    def fix_via_orm(self, force=False):
        """Fix via Django ORM for more granular control"""
        self.stdout.write('   🐍 Running ORM fixes...')
        
        try:
            fixed_count = 0
            scan_jobs = ScanJob.objects.all()
            
            for scan in scan_jobs:
                try:
                    # Use the clean_duration_data method
                    was_fixed = scan.clean_duration_data()
                    
                    # If force mode, also fix completed scans without proper duration
                    if force and scan.status == 'completed' and not scan.scan_duration:
                        if scan.started_at and scan.finished_at:
                            # Recalculate duration
                            scan.safe_calculate_duration()
                            was_fixed = True
                    
                    if was_fixed:
                        scan.save()
                        fixed_count += 1
                        
                except Exception as e:
                    self.stdout.write(f'   ⚠️ Error fixing scan {scan.id}: {e}')
                    continue
            
            self.stdout.write(f'   • ORM fixed: {fixed_count} records')
            return fixed_count
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ ORM fix failed: {e}'))
            return 0
    
    def verify_fix(self):
        """Verify that all corrupt data is fixed"""
        self.stdout.write('   ✅ Verifying fixes...')
        
        try:
            with connection.cursor() as cursor:
                # Check for remaining corrupt data
                cursor.execute("""
                    SELECT COUNT(*) FROM sast_report_scanjob 
                    WHERE scan_duration IS NOT NULL 
                    AND scan_duration NOT LIKE '%%days%%'
                """)
                remaining_corrupt = cursor.fetchone()[0]
                
                # Check for valid data
                cursor.execute("""
                    SELECT COUNT(*) FROM sast_report_scanjob 
                    WHERE scan_duration IS NOT NULL 
                    AND scan_duration LIKE '%%days%%'
                """)
                valid_durations = cursor.fetchone()[0]
                
                self.stdout.write(f'   • Valid durations: {valid_durations}')
                self.stdout.write(f'   • Remaining corrupt: {remaining_corrupt}')
                
                return remaining_corrupt
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Verification failed: {e}'))
            return -1
