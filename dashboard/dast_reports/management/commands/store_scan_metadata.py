from django.core.management.base import BaseCommand
from dast_reports.models import DASTScan

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--scan-id', type=int, required=True)
        parser.add_argument('--build-number', type=int, required=True)
        parser.add_argument('--target-url', type=str, required=True)

    def handle(self, *args, **options):
        scan = DASTScan.objects.get(id=options['scan_id'])
        scan.jenkins_build_number = options['build_number']
        scan.json_report_path = f"/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-{options['build_number']}.json"
        scan.target_url = options['target_url']
        scan.save()
        self.stdout.write(f"Stored metadata for scan {scan.id}")
