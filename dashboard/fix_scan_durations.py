# fix_scan_durations.py
from django.utils import timezone
from datetime import timedelta
from sast_report.models import ScanJob

def fix_scan_durations():
    """Perbaiki semua data scan_duration yang corrupt"""
    scans = ScanJob.objects.all()
    fixed_count = 0
    
    for scan in scans:
        try:
            # Cek jika scan_duration bukan timedelta
            if scan.scan_duration and not isinstance(scan.scan_duration, timedelta):
                print(f"🔄 Fixing duration for scan {scan.id}")
                
                # Coba hitung ulang duration
                if not scan.calculate_duration():
                    # Jika tidak bisa dihitung, set ke None
                    scan.scan_duration = None
                    scan.save(update_fields=['scan_duration'])
                
                fixed_count += 1
                
        except Exception as e:
            print(f"❌ Error fixing scan {scan.id}: {e}")
            # Force set to None jika ada error
            scan.scan_duration = None
            scan.save(update_fields=['scan_duration'])
            fixed_count += 1
    
    print(f"✅ Fixed {fixed_count} scan duration records")
    return fixed_count

# Jalankan: python manage.py shell < fix_scan_durations.py
