from django.core.management.base import BaseCommand
from dast_reports.models import DASTScan
import json
import os
from django.db import transaction

class Command(BaseCommand):
    help = 'Update DAST vulnerabilities from JSON report file'
    
    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to ZAP JSON report file')
        parser.add_argument('target_url', type=str, help='Target URL that was scanned')
        parser.add_argument('--scan-id', type=int, help='Specific scan ID to update (optional)')

    def handle(self, *args, **options):
        json_file = options['json_file']
        target_url = options['target_url']
        scan_id = options['scan_id']
        
        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(f"❌ JSON file not found: {json_file}"))
            return

        try:
            # Cari scan berdasarkan scan_id atau target_url
            if scan_id:
                scan = DASTScan.objects.get(id=scan_id)
            else:
                scan = DASTScan.objects.filter(target_url=target_url).order_by('-scan_date').first()
                if not scan:
                    self.stdout.write(self.style.ERROR(f"❌ No scan found for target: {target_url}"))
                    return
            
            self.stdout.write(f"📊 Updating scan ID {scan.id} for target: {target_url}")
            
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Reset counters
            high_count = 0
            medium_count = 0
            low_count = 0
            info_count = 0

            # Parse alerts dari struktur ZAP JSON
            if 'site' in data and isinstance(data['site'], list):
                for site in data['site']:
                    if 'alerts' in site and isinstance(site['alerts'], list):
                        for alert in site['alerts']:
                            riskcode = alert.get('riskcode', '0')
                            
                            # Map riskcode ke severity level
                            if riskcode == '3':  # High
                                high_count += 1
                            elif riskcode == '2':  # Medium
                                medium_count += 1
                            elif riskcode == '1':  # Low
                                low_count += 1
                            else:  # Informational (0) atau unknown
                                info_count += 1

            # Update scan object
            with transaction.atomic():
                scan.high_vulnerabilities = high_count
                scan.medium_vulnerabilities = medium_count
                scan.low_vulnerabilities = low_count
                scan.informational_vulnerabilities = info_count
                
                # Hitung total vulnerabilities
                total_vulns = high_count + medium_count + low_count + info_count
                scan.vulnerabilities_found = total_vulns
                
                scan.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Updated scan {scan.id}: "
                    f"H:{high_count}, M:{medium_count}, L:{low_count}, I:{info_count}"
                )
            )

        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"❌ Invalid JSON format in {json_file}"))
        except DASTScan.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Scan ID {scan_id} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error updating from JSON: {str(e)}"))
