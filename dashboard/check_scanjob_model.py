import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob

def inspect_scanjob_model():
    print("🔍 INSPECTING SCANJOB MODEL STRUCTURE")
    print("=" * 50)
    
    # Get all fields of ScanJob model
    fields = ScanJob._meta.get_fields()
    
    print("📋 SCANJOB FIELDS:")
    for field in fields:
        field_info = f"  - {field.name} ({field.get_internal_type()})"
        if field.is_relation:
            field_info += f" -> {field.related_model.__name__}"
        print(field_info)
    
    # Check a sample ScanJob instance
    if ScanJob.objects.exists():
        sample = ScanJob.objects.first()
        print(f"\n📄 SAMPLE SCANJOB INSTANCE (#{sample.id}):")
        for field in fields:
            if not field.is_relation and not field.auto_created:
                try:
                    value = getattr(sample, field.name)
                    print(f"  - {field.name}: {value}")
                except:
                    print(f"  - {field.name}: <error>")
    
    print(f"\n💡 TOTAL SCANJOBS IN DATABASE: {ScanJob.objects.count()}")

if __name__ == '__main__':
    inspect_scanjob_model()
