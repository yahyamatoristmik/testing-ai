#!/usr/bin/env python3
import os
import sys
import django
import json

# Setup Django environment
sys.path.append('/home/dj/ai-evaluator/dashboard')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.contrib.admin.sites import site
from dast_reports.models import DASTScan
from dast_reports.admin import DASTScanAdmin

def test_json_structure():
    """Test struktur JSON file"""
    json_path = "/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-167.json"
    
    print("=== TESTING JSON STRUCTURE ===")
    print(f"File: {json_path}")
    print(f"Exists: {os.path.exists(json_path)}")
    
    if not os.path.exists(json_path):
        print("❌ File not found!")
        return
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    print(f"Root keys: {list(data.keys())}")
    
    if 'site' in data and data['site']:
        site = data['site'][0]
        print(f"Site keys: {list(site.keys())}")
        
        if 'alerts' in site:
            alerts = site['alerts']
            print(f"Number of alerts: {len(alerts)}")
            
            # Count by risk code
            risk_counts = {'3': 0, '2': 0, '1': 0, 'other': 0}
            for i, alert in enumerate(alerts[:10]):  # First 10 alerts
                riskcode = alert.get('riskcode', 'other')
                risk_counts[riskcode] = risk_counts.get(riskcode, 0) + 1
                print(f"  {i+1}. {alert.get('name')} - Risk: {riskcode}")
            
            print(f"\n📊 Risk code summary:")
            print(f"  High (3): {risk_counts['3']}")
            print(f"  Medium (2): {risk_counts['2']}")
            print(f"  Low (1): {risk_counts['1']}")
            print(f"  Other: {risk_counts['other']}")

def test_update_method():
    """Test _update_from_json method"""
    print("\n=== TESTING _update_from_json METHOD ===")
    
    # Get scan by ID 167 (sesuai dengan file JSON)
    try:
        scan = DASTScan.objects.get(id=167)
        print(f"✅ Found scan: ID {scan.id} - {scan.name}")
    except DASTScan.DoesNotExist:
        print("❌ Scan ID 167 not found! Available scans:")
        scans = DASTScan.objects.all().order_by('-id')
        for s in scans:
            print(f"  ID {s.id}: {s.name}")
        return
    
    json_path = "/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-167.json"
    print(f"JSON path: {json_path}")
    
    if not os.path.exists(json_path):
        print("❌ JSON file not found!")
        return
    
    # Initialize admin properly
    admin = DASTScanAdmin(DASTScan, site)
    
    print(f"\n📊 BEFORE:")
    print(f"  High: {scan.high_vulnerabilities}")
    print(f"  Medium: {scan.medium_vulnerabilities}")
    print(f"  Low: {scan.low_vulnerabilities}")
    print(f"  Info: {scan.informational_vulnerabilities}")
    
    success = admin._update_from_json(scan, json_path)
    print(f"✅ Update success: {success}")
    
    scan.refresh_from_db()
    print(f"\n📊 AFTER:")
    print(f"  High: {scan.high_vulnerabilities}")
    print(f"  Medium: {scan.medium_vulnerabilities}")
    print(f"  Low: {scan.low_vulnerabilities}")
    print(f"  Info: {scan.informational_vulnerabilities}")
    print(f"  Total: {scan.vulnerabilities_found}")

def manual_update_scan_167():
    """Manual update untuk scan ID 167"""
    print("\n=== MANUAL UPDATE FOR SCAN 167 ===")
    
    try:
        scan = DASTScan.objects.get(id=167)
    except DASTScan.DoesNotExist:
        print("❌ Scan ID 167 not found!")
        return
    
    json_path = "/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-167.json"
    
    if not os.path.exists(json_path):
        print("❌ JSON file not found!")
        return
    
    # Manual parsing dan update
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    high_count = 0
    medium_count = 0
    low_count = 0
    info_count = 0

    if 'site' in data and isinstance(data['site'], list):
        for site in data['site']:
            if 'alerts' in site and isinstance(site['alerts'], list):
                for alert in site['alerts']:
                    riskcode = alert.get('riskcode', '0')
                    if riskcode == '3':
                        high_count += 1
                    elif riskcode == '2':
                        medium_count += 1
                    elif riskcode == '1':
                        low_count += 1
                    else:
                        info_count += 1

    # Update scan manually
    scan.high_vulnerabilities = high_count
    scan.medium_vulnerabilities = medium_count
    scan.low_vulnerabilities = low_count
    scan.informational_vulnerabilities = info_count
    scan.vulnerabilities_found = high_count + medium_count + low_count + info_count
    scan.save()

    print(f"✅ Manual update successful!")
    print(f"  High: {high_count}")
    print(f"  Medium: {medium_count}")
    print(f"  Low: {low_count}")
    print(f"  Info: {info_count}")
    print(f"  Total: {scan.vulnerabilities_found}")

if __name__ == "__main__":
    test_json_structure()
    test_update_method()
    manual_update_scan_167()
