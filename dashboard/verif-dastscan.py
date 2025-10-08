from dast_reports.models import DASTScan

# Check scan terupdate
scan = DASTScan.objects.get(id=13)
print(f"Scan ID: {scan.id}")
print(f"Target URL: {scan.target_url}")
print(f"Build Number: {scan.jenkins_build_number}")
print(f"JSON Path: {scan.json_report_path}")
print(f"Vulnerabilities - H:{scan.high_vulnerabilities}, M:{scan.medium_vulnerabilities}, L:{scan.low_vulnerabilities}")
print(f"Total: {scan.vulnerabilities_found}")
