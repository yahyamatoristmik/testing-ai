from django.core.management.base import BaseCommand
from dast_reports.models import DASTScan
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

class Command(BaseCommand):
    help = 'Clean up duplicate scans based on target URL and status'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        with transaction.atomic():
            if dry_run:
                self.stdout.write(
                    self.style.WARNING("DRY RUN MODE - No changes will be made")
                )
            
            # Strategy 1: Hapus duplicate running scans untuk URL yang sama
            self.cleanup_running_duplicates(dry_run)
            
            # Strategy 2: Hapus old completed scans (keep only latest 2)
            self.cleanup_old_completed_scans(dry_run)
            
            # Strategy 3: Hapus pending scans yang sudah lama
            self.cleanup_old_pending_scans(dry_run)
            
            if dry_run:
                self.stdout.write(
                    self.style.WARNING("Dry run completed. Use without --dry-run to execute changes")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("Duplicate scan cleanup completed successfully!")
                )

    def cleanup_running_duplicates(self, dry_run):
        """Hapus duplicate running scans untuk URL yang sama"""
        # Cari URL yang memiliki multiple running scans
        running_duplicates = DASTScan.objects.filter(status='running').values(
            'target_url'
        ).annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        for url_data in running_duplicates:
            target_url = url_data['target_url']
            running_scans = DASTScan.objects.filter(
                target_url=target_url, 
                status='running'
            ).order_by('-scan_date')
            
            # Keep the newest running scan, delete older ones
            if running_scans.count() > 1:
                newest_scan = running_scans.first()
                old_running_scans = running_scans.exclude(id=newest_scan.id)
                
                self.stdout.write(
                    self.style.WARNING(
                        f"Found {old_running_scans.count()} duplicate RUNNING scans for {target_url}. "
                        f"Keeping newest scan ID {newest_scan.id} (scan date: {newest_scan.scan_date})"
                    )
                )
                
                for scan in old_running_scans:
                    self.stdout.write(
                        f"  - Would delete scan ID {scan.id} (scan date: {scan.scan_date})"
                    )
                    if not dry_run:
                        scan.delete()

    def cleanup_old_completed_scans(self, dry_run):
        """Hapus completed scans yang lama, keep only latest 2 per URL"""
        # Cari URL yang memiliki multiple completed scans
        completed_duplicates = DASTScan.objects.filter(status='completed').values(
            'target_url'
        ).annotate(
            count=Count('id')
        ).filter(count__gt=2)  # Keep only latest 2 completed scans per URL
        
        for url_data in completed_duplicates:
            target_url = url_data['target_url']
            completed_scans = DASTScan.objects.filter(
                target_url=target_url, 
                status='completed'
            ).order_by('-completed_date')
            
            # Keep only 2 latest completed scans
            if completed_scans.count() > 2:
                scans_to_keep = completed_scans[:2]
                scans_to_delete = completed_scans[2:]
                
                self.stdout.write(
                    self.style.WARNING(
                        f"Found {scans_to_delete.count()} old COMPLETED scans for {target_url}. "
                        f"Keeping latest 2 scans: {[s.id for s in scans_to_keep]}"
                    )
                )
                
                for scan in scans_to_delete:
                    self.stdout.write(
                        f"  - Would delete old completed scan ID {scan.id} (completed: {scan.completed_date})"
                    )
                    if not dry_run:
                        scan.delete()

    def cleanup_old_pending_scans(self, dry_run):
        """Hapus pending scans yang sudah lebih dari 24 jam"""
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        
        old_pending_scans = DASTScan.objects.filter(
            status='pending',
            created_at__lt=twenty_four_hours_ago
        )
        
        if old_pending_scans.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Found {old_pending_scans.count()} old PENDING scans (older than 24 hours)"
                )
            )
            
            for scan in old_pending_scans:
                self.stdout.write(
                    f"  - Would delete old pending scan ID {scan.id} for {scan.target_url} "
                    f"(created: {scan.created_at})"
                )
                if not dry_run:
                    scan.delete()
