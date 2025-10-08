from django.core.management.base import BaseCommand
from dast_reports.models import DASTScan
import json
import os
from django.db import transaction

class Command(BaseCommand):
    help = 'Update all scans with vulnerabilities from JSON reports'
    
    def handle(self, *args, **options):
        self.stdout.write("=== UPDATING ALL SCANS ===")
        scans = DASTScan.objects.all().order_by('-id')
        
        for scan in scans:
            if scan.jenkins_build_number:
                self.stdout.write(f"\nUpdating scan {scan.id} (Build #{scan.jenkins_build_number})...")
                self.update_scan(scan)
            else:
                self.stdout.write(f"\nSkipping scan {scan.id} (No build number)")
        
        self.stdout.write(self.style.SUCCESS("\n🎉 All scans updated!"))
    
    def update_scan(self, scan):
        json_path = f"/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-{scan.jenkins_build_number}.json"
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.WARNING(f"JSON not found: {json_path}"))
            return False
        
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)

            high_count = 0
            medium_count = 0
            low_count = 0
            info_count = 0

            if 'site' in data and isinstance(data['site'], list):
                for site_data in data['site']:
                    if 'alerts' in site_data and isinstance(site_data['alerts'], list):
                        for alert in site_data['alerts']:
                            riskcode = alert.get('riskcode', '0')
                            if riskcode == '3': high_count += 1
                            elif riskcode == '2': medium_count += 1
                            elif riskcode == '1': low_count += 1
                            else: info_count += 1

            with transaction.atomic():
                scan.high_vulnerabilities = high_count
                scan.medium_vulnerabilities = medium_count
                scan.low_vulnerabilities = low_count
                scan.informational_vulnerabilities = info_count
                scan.vulnerabilities_found = high_count + medium_count + low_count + info_count
                scan.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Scan {scan.id}: H:{high_count}, M:{medium_count}, L:{low_count}, I:{info_count}"
                )
            )
            return True

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error updating scan {scan.id}: {e}"))
            return False
