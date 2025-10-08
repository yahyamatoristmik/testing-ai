#!/usr/bin/env python3
import os
import sys
import django

# Setup Django environment
sys.path.append('/home/dj/ai-evaluator/dashboard')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dast_reports.models import DASTScan

print("=== FINAL VERIFICATION ===")
scans = DASTScan.objects.all().order_by('-id')

for scan in scans:
    if scan.jenkins_build_number:
        status = "✅" if scan.high_vulnerabilities > 0 or scan.medium_vulnerabilities > 0 else "⚠️ "
        print(f"{status} ID {scan.id}: Build #{scan.jenkins_build_number}")
        print(f"   Vulnerabilities: H:{scan.high_vulnerabilities}, M:{scan.medium_vulnerabilities}, L:{scan.low_vulnerabilities}")
        print(f"   Total: {scan.vulnerabilities_found}")
        
        # Check if JSON file exists
        json_path = f"/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-{scan.jenkins_build_number}.json"
        file_exists = os.path.exists(json_path)
        print(f"   JSON File: {'✅ Exists' if file_exists else '❌ Missing'} - {json_path}")
    else:
        print(f"❌ ID {scan.id}: No build number")
    print()
