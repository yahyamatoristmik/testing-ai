from dast_reports.admin import DASTScanAdmin
from django.contrib.admin.sites import site

admin = DASTScanAdmin(DASTScan, site)

# Cek method yang available
methods = [method for method in dir(admin) if not method.startswith('_')]
print("Available methods in DASTScanAdmin:")
for method in sorted(methods):
    print(f"  - {method}")

# Cek khusus method update
update_methods = [m for m in methods if 'update' in m.lower() or 'json' in m.lower()]
print("\nUpdate-related methods:")
for method in update_methods:
    print(f"  - {method}")
