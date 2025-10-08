import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')  # Ganti 'your_project' dengan nama project yang benar
django.setup()

# Cek semua models yang tersedia
from django.apps import apps

print("📋 AVAILABLE MODELS:")
for model in apps.get_models():
    print(f"  - {model._meta.app_label}.{model.__name__}")

print("\n🔍 SAST REPORT MODELS:")
try:
    from sast_report import models
    for name in dir(models):
        if not name.startswith('_') and not name.islower():
            print(f"  - {name}")
except ImportError as e:
    print(f"❌ Error: {e}")
