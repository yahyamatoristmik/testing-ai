# dast_report/management/commands/update_scan_from_json.py
import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from dast_report.models import DASTScan

class Command(BaseCommand):
    help = 'Update DASTScan from JSON report file (Automated from Jenkins)'
    
    def add_arguments(self, parser):
        parser.add_argument('--target', type=str, required=True, help='Target URL (e.g., http://investpro.id)')
        parser.add_argument('--json-file', type=str, required=True, help='Path to JSON report file')
        parser.add_argument('--scan-name', type=str, help='Custom scan name')
    
    def handle(self, *args, **options):
        target_url = options['target']
        json_file_path = options['json_file']
        scan_name = options.get('scan_name', f"ZAP Scan - {target_url}")
        
        self.stdout.write(f"Updating scan for: {target_url}")
        self.stdout.write(f"JSON file: {json_file_path}")
        
        try:
            # Baca file JSON
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cari atau buat DASTScan record
            scan, created = DASTScan.objects.get_or_create(
                target_url=target_url,
                defaults={
                    'name': scan_name,
                    'scan_type': 'full',
                    'status': 'completed',
                    'completed_date': timezone.now()
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created new scan record"))
            else:
                # Update existing record
                scan.status = 'completed'
                scan.completed_date = timezone.now()
                self.stdout.write(self.style.SUCCESS(f"Updated existing scan record"))
            
            # Update vulnerability counts dari summary
            if 'summary' in data:
                summary = data['summary']
                scan.high_vulnerabilities = summary.get('Tinggi', 0)
                scan.medium_vulnerabilities = summary.get('Sedang', 0)
                scan.low_vulnerabilities = summary.get('Rendah', 0)
                scan.informational_vulnerabilities = summary.get('Informasi', 0)
                
                self.stdout.write(f"Vulnerability counts:")
                self.stdout.write(f"  High: {scan.high_vulnerabilities}")
                self.stdout.write(f"  Medium: {scan.medium_vulnerabilities}")
                self.stdout.write(f"  Low: {scan.low_vulnerabilities}")
            
            # Simpan results JSON
            scan.results = data
            
            # Save akan otomatis hitung vulnerabilities_found
            scan.save()
            
            self.stdout.write(self.style.SUCCESS(
                f"Successfully updated scan ID: {scan.id}"
            ))
            self.stdout.write(f"Total vulnerabilities: {scan.vulnerabilities_found}")
            self.stdout.write(f"Risk score: {scan.risk_score}")
            self.stdout.write(f"Admin URL: https://sentinel.investpro.id/admin/dast_reports/dastscan/{scan.id}/change/")
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"JSON file not found: {json_file_path}"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Invalid JSON file: {json_file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
