#!/usr/bin/env python3
import os
import sys
import django
import json

sys.path.append('/home/dj/ai-evaluator/dashboard')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dast_reports.models import DASTScan
from django.db import transaction

def manual_update_from_json(scan, json_file_path):
    """Manual implementation of JSON parsing"""
    try:
        with open(json_file_path, 'r') as f:
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

        print(f"✅ Successfully updated vulnerabilities: H:{high_count}, M:{medium_count}, L:{low_count}, I:{info_count}")
        return True

    except json.JSONDecodeError:
        print(f"❌ Invalid JSON format in {json_file_path}")
        return False
    except Exception as e:
        print(f"❌ Error updating from JSON: {str(e)}")
        return False

# Test manual update
scan = DASTScan.objects.get(id=13)
json_path = "/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-167.json"

print(f"Testing scan ID {scan.id}, Build #{scan.jenkins_build_number}")
print(f"Before - High: {scan.high_vulnerabilities}, Medium: {scan.medium_vulnerabilities}")

success = manual_update_from_json(scan, json_path)

if success:
    scan.refresh_from_db()
    print(f"After - High: {scan.high_vulnerabilities}, Medium: {scan.medium_vulnerabilities}")
