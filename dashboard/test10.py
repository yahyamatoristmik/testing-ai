#!/usr/bin/env python3
import os
import sys
import django

# Setup Django environment
sys.path.append('/home/dj/ai-evaluator/dashboard')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dast_reports.models import DASTScan
from dast_reports.admin import DASTScanAdmin
from django.contrib.admin.sites import site

print("=== TESTING ADMIN METHOD ===")

# Test dengan scan yang sudah ada build number
scan = DASTScan.objects.get(id=13)
print(f"Testing scan ID {scan.id}, Build #{scan.jenkins_build_number}")

admin = DASTScanAdmin(DASTScan, site)

print(f"Before - High: {scan.high_vulnerabilities}, Medium: {scan.medium_vulnerabilities}")

success = admin._update_from_json(scan, scan.json_report_path)
print(f"Update success: {success}")

scan.refresh_from_db()
print(f"After - High: {scan.high_vulnerabilities}, Medium: {scan.medium_vulnerabilities}")
