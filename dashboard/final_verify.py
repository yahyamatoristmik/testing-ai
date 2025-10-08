#!/usr/bin/env python3
import os
import sys
import django

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
    else:
        print(f"❌ ID {scan.id}: No build number")
    print()
