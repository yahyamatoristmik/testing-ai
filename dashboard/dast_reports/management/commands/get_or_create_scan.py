from django.core.management.base import BaseCommand
from dast_reports.models import DASTScan
from django.utils import timezone

class Command(BaseCommand):
    help = 'Get or create DASTScan record and return scan ID'
    
    def add_arguments(self, parser):
        parser.add_argument('--target-url', type=str, required=True)
        parser.add_argument('--scan-name', type=str, required=True)
        parser.add_argument('--quiet', action='store_true', help='Output only scan ID')

    def handle(self, *args, **options):
        target_url = options['target_url'].rstrip('/')
        scan_name = options['scan_name']
        quiet = options['quiet']
        
        scan = DASTScan.objects.filter(
            target_url=target_url, 
            status__in=['running', 'pending', 'completed']
        ).order_by('-scan_date').first()

        if not scan:
            scan = DASTScan(
                name=scan_name,
                target_url=target_url,
                scan_type='full',
                scan_date=timezone.now(),
                status='running',
                active=True,
                scheduled=False,
                high_vulnerabilities=0,
                medium_vulnerabilities=0,
                low_vulnerabilities=0,
                informational_vulnerabilities=0,
                vulnerabilities_found=0,
                pages_crawled=0,
                requests_made=0,
                scan_config={}
            )
            scan.save()
            if not quiet:
                self.stdout.write(f"Created new scan: {scan.id}")
        else:
            scan.status = 'running'
            scan.save()
            if not quiet:
                self.stdout.write(f"Using existing scan: {scan.id}")
        
        # Output HANYA scan ID (untuk ditangkap oleh Jenkins)
        self.stdout.write(str(scan.id))
