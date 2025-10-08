import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.conf import settings

def check_static_and_middleware():
    print("🔧 CHECKING STATIC FILES & MIDDLEWARE")
    print("=" * 50)
    
    print("📋 INSTALLED APPS:")
    for app in settings.INSTALLED_APPS:
        if 'static' in app or 'sast' in app or 'dashboard' in app:
            print(f"   ✅ {app}")
    
    print(f"\n📁 STATIC SETTINGS:")
    print(f"   STATIC_URL: {settings.STATIC_URL}")
    print(f"   STATIC_ROOT: {getattr(settings, 'STATIC_ROOT', 'Not set')}")
    
    print(f"\n🔧 MIDDLEWARE:")
    for middleware in settings.MIDDLEWARE:
        if 'static' in middleware or 'auth' in middleware:
            print(f"   ✅ {middleware}")
    
    print(f"\n🌐 ALLOWED HOSTS: {settings.ALLOWED_HOSTS}")
    
    # Check template directories
    print(f"\n📝 TEMPLATE DIRS:")
    for template_dir in settings.TEMPLATES[0]['DIRS']:
        print(f"   📁 {template_dir}")

if __name__ == '__main__':
    check_static_and_middleware()
