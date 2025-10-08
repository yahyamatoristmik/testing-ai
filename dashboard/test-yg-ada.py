from dast_reports.models import DASTScan

# Manual mapping berdasarkan file yang ada
mapping = {
    13: 167,  # scan_id: build_number
    12: 166,
    11: 165, 
    10: 164,
    8: 163,
    7: 158
}

for scan_id, build_number in mapping.items():
    try:
        scan = DASTScan.objects.get(id=scan_id)
        scan.jenkins_build_number = build_number
        scan.json_report_path = f"/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-{build_number}.json"
        scan.save()
        print(f"✅ Updated scan {scan_id} with build {build_number}")
    except:
        print(f"❌ Failed to update scan {scan_id}")
