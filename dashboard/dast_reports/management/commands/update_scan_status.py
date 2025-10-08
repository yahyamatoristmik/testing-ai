from django.core.management.base import BaseCommand
from dast_reports.models import DASTScan
from django.utils import timezone

class Command(BaseCommand):
    help = 'Update scan status'
    
    def add_arguments(self, parser):
        parser.add_argument('--scan-id', type=int, required=True)
        parser.add_argument('--status', type=str, required=True)
        parser.add_argument('--quiet', action='store_true', help='Output only success message')

    def handle(self, *args, **options):
        try:
            scan = DASTScan.objects.get(id=options['scan_id'])
            scan.status = options['status']
            scan.completed_date = timezone.now()
            scan.save()
            
            if not options['quiet']:
                self.stdout.write(self.style.SUCCESS(f"Updated scan status to {options['status']}: {scan.id}"))
            else:
                self.stdout.write("success")
                
        except DASTScan.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Scan ID {options['scan_id']} not found"))
