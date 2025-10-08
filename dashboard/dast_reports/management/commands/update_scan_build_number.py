from django.core.management.base import BaseCommand
from dast_reports.models import DASTScan

class Command(BaseCommand):
    help = 'Update DASTScan with Jenkins build number and JSON path'
    
    def add_arguments(self, parser):
        parser.add_argument('--scan-id', type=int, required=True, help='Database Scan ID')
        parser.add_argument('--build-number', type=int, required=True, help='Jenkins Build Number')
        parser.add_argument('--json-path', type=str, required=True, help='Full path to JSON report')
        parser.add_argument('--quiet', action='store_true', help='Output only success message')

    def handle(self, *args, **options):
        try:
            scan = DASTScan.objects.get(id=options['scan_id'])
            scan.jenkins_build_number = options['build_number']
            scan.json_report_path = options['json_path']
            scan.save()
            
            if not options['quiet']:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Updated scan ID {scan.id} with build #{options['build_number']}"
                    )
                )
            else:
                self.stdout.write("success")
            
        except DASTScan.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Scan ID {options['scan_id']} not found!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
