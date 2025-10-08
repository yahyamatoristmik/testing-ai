from dast_reports.models import DASTScan

# Clear build number untuk scan yang duplicate
scan = DASTScan.objects.get(id=13)
scan.jenkins_build_number = None
scan.json_report_path = ""
scan.save()
print("✅ Cleared duplicate build number from scan 13")

# Sekarang update dengan benar
scan.jenkins_build_number = 167
scan.json_report_path = "/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-167.json"
scan.save()
print("✅ Updated scan 13 with build 167")
