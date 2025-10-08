#!/usr/bin/env python
import os
import django
import sys

# Setup Django environment
sys.path.append('/home/dj/ai-evaluator/dashboard')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob
from datetime import timedelta

def main():
    print("🔧 Memulai perbaikan data scan_duration...")
    
    # Hitung total
    total_scans = ScanJob.objects.count()
    print(f"📊 Total ScanJob: {total_scans}")
    
    # Identifikasi data corrupt
    corrupt_data = []
    for scan in ScanJob.objects.all():
        if scan.scan_duration and not isinstance(scan.scan_duration, timedelta):
            corrupt_data.append({
                'id': scan.id,
                'duration_type': type(scan.scan_duration),
                'duration_value': scan.scan_duration
            })
    
    print(f"⚠️  Data corrupt ditemukan: {len(corrupt_data)}")
    
    for data in corrupt_data:
        print(f"   - Scan {data['id']}: {data['duration_type']} = {data['duration_value']}")
    
    # Konfirmasi
    if corrupt_data:
        confirm = input("🚨 Lanjutkan perbaikan? (y/n): ")
        if confirm.lower() != 'y':
            print("❌ Dibatalkan")
            return
    
    # Emergency cleanup
    print("🔄 Membersihkan data...")
    updated = ScanJob.objects.all().update(scan_duration=None)
    
    print(f"✅ Berhasil membersihkan {updated} records")
    print("🎉 Perbaikan selesai!")
    
    # Verifikasi
    print("\n🔍 Verifikasi:")
    for scan in ScanJob.objects.all()[:5]:  # Cek 5 data pertama
        print(f"   Scan {scan.id}: duration = {scan.scan_duration}")

if __name__ == "__main__":
    main()
