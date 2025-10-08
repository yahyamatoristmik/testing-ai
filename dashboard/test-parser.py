from dast_reports.models import DASTScan
import glob
import re

# List semua scan
scans = DASTScan.objects.all().order_by('-id')
print("📋 Scans in database:")
for scan in scans:
    print(f"  ID: {scan.id}, Name: '{scan.name}', Created: {scan.created_at}")

# List semua JSON files
json_files = glob.glob("/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-*.json")
print("\n📂 JSON files available:")
for file_path in json_files:
    # Extract build number dari filename
    match = re.search(r'zap-report-(\d+)\.json', file_path)
    if match:
        build_number = match.group(1)
        print(f"  Build: {build_number}, File: {file_path}")

# Cari pattern atau correlation
print("\n🔍 Looking for correlations...")
for file_path in json_files:
    match = re.search(r'zap-report-(\d+)\.json', file_path)
    if match:
        build_number = match.group(1)
        # Coba cari scan dengan created date yang mirip
        # atau dengan name yang mengandung build number
        pass
