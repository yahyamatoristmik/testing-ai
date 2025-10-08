# dast_report/management/commands/auto_update_scan.py
import json
import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from dast_report.models import DASTScan

class Command(BaseCommand):
    help = 'Automatically update scan results from JSON file'
    
    def add_arguments(self, parser):
        parser.add_argument('--json-path', type=str, required=True, 
                          help='Path to JSON report file')
    
    def handle(self, *args, **options):
        json_path = options['json_path']
        
        # Cari scan yang sedang "running" untuk diupdate
        running_scans = DASTScan.objects.filter(status='running')
        
        if not running_scans.exists():
            self.stdout.write("❌ No running scans found")
            return
        
        # Ambil scan terbaru yang running
        latest_scan = running_scans.latest('updated_at')
        
        try:
            # Baca file JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.stdout.write(f"Updating scan: {latest_scan.target_url}")
            
            # Update vulnerability counts dari summary
            if 'summary' in data:
                summary = data['summary']
                latest_scan.high_vulnerabilities = summary.get('Tinggi', 0)
                latest_scan.medium_vulnerabilities = summary.get('Sedang', 0)
                latest_scan.low_vulnerabilities = summary.get('Rendah', 0)
                
                self.stdout.write(f"High: {latest_scan.high_vulnerabilities}")
                self.stdout.write(f"Medium: {latest_scan.medium_vulnerabilities}") 
                self.stdout.write(f"Low: {latest_scan.low_vulnerabilities}")
            
            # Update status dan results
            latest_scan.status = 'completed'
            latest_scan.completed_date = timezone.now()
            latest_scan.results = data
            
            latest_scan.save()
            
            self.stdout.write(self.style.SUCCESS(
                f"✅ Successfully updated scan ID: {latest_scan.id}"
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
