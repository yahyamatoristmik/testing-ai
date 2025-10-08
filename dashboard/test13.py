#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
sys.path.append('/home/dj/ai-evaluator/dashboard')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from dast_reports.models import DASTScan

print("=== FIXING SCAN 13 ===")

# Clear existing build number untuk avoid duplicate
scan13 = DASTScan.objects.get(id=13)
scan13.jenkins_build_number = None
scan13.json_report_path = ""
scan13.save()
print("✅ Cleared existing values")

# Set baru
scan13.jenkins_build_number = 167
scan13.json_report_path = "/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-167.json"
scan13.save()
print("✅ Set new values for scan 13")

# Verify
scan13.refresh_from_db()
print(f"Scan 13 - Build: {scan13.jenkins_build_number}, Path: {scan13.json_report_path}")
