# clean_duration_data.py
from sast_report.models import ScanJob

def clean_scan_durations():
    for scan in ScanJob.objects.all():
        if scan.scan_duration:
            try:
                # Jika scan_duration adalah timedelta, konversi ke seconds
                if hasattr(scan.scan_duration, 'total_seconds'):
                    scan.scan_duration = scan.scan_duration.total_seconds()
                else:
                    scan.scan_duration = float(scan.scan_duration)
                scan.save()
                print(f"Fixed scan {scan.id}: {scan.scan_duration}")
            except Exception as e:
                print(f"Error fixing scan {scan.id}: {e}")
                scan.scan_duration = None
                scan.save()

clean_scan_durations()
