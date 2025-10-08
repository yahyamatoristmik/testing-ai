import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob

def fix_scan_duration_issue():
    print("🔧 FIXING SCAN DURATION ISSUE")
    print("=" * 50)
    
    # Set semua scan_duration menjadi NULL untuk menghindari error
    scans_with_duration = ScanJob.objects.exclude(scan_duration__isnull=True)
    print(f"📊 Scans with problematic scan_duration: {scans_with_duration.count()}")
    
    for scan in scans_with_duration:
        scan.scan_duration = None
        scan.save()
        print(f"✅ Fixed scan #{scan.id}")
    
    print(f"\n🎯 SEMUA SCAN_DURATION TELAH DI-SET NULL")
    print("💡 Sekarang worker dan queries seharusnya bekerja tanpa error")

if __name__ == '__main__':
    fix_scan_duration_issue()
