#!/usr/bin/env python3
import os
import sys
import django

sys.path.append('/home/dj/ai-evaluator/dashboard')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dast_reports.models import DASTScan

print("=== SCAN VERIFICATION ===")
scans = DASTScan.objects.all().order_by('-id')

for scan in scans:
    status = "✅" if scan.jenkins_build_number else "❌"
    print(f"{status} ID {scan.id}: {scan.name}")
    if scan.jenkins_build_number:
        print(f"   Build: #{scan.jenkins_build_number}")
        print(f"   JSON: {scan.json_report_path}")
        print(f"   Vulns: H:{scan.high_vulnerabilities}, M:{scan.medium_vulnerabilities}, L:{scan.low_vulnerabilities}")
    print()
