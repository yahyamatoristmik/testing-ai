from django.core.management.base import BaseCommand
from sast_report.models import ScanJob
from sast_report.semgrep_scanner import run_semgrep_scan

class Command(BaseCommand):
    help = 'Run pending scan jobs using Semgrep'
    
    def add_arguments(self, parser):
        parser.add_argument('--job-id', type=int, help='Specific job ID to scan')
    
    def handle(self, *args, **options):
        job_id = options.get('job_id')
        
        if job_id:
            jobs = ScanJob.objects.filter(id=job_id, status='pending')
        else:
            jobs = ScanJob.objects.filter(status='pending')
        
        self.stdout.write(f"Found {jobs.count()} pending jobs")
        
        for job in jobs:
            self.stdout.write(f"Processing job {job.id}: {job.repository.name}")
            success = run_semgrep_scan(job.id)
            
            if success:
                self.stdout.write(f"✓ Job {job.id} completed successfully")
            else:
                self.stdout.write(f"✗ Job {job.id} failed")
