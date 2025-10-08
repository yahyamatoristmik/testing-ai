import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
import django
django.setup()
from sast_report.models import ScanJob
ScanJob.objects.all().update(scan_duration=None)
print("✅ Fixed! Now check your admin page.")
