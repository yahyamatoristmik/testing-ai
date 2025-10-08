import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User

def test_dashboard_view():
    print("🌐 TESTING DASHBOARD VIEW")
    print("=" * 50)
    
    try:
        # Import view setelah setup Django
        from dashboard.views import sast_report_view  # Ganti dengan nama view yang benar
        
        # Create request dengan host yang benar
        factory = RequestFactory()
        request = factory.get('/sast-report/')
        request.META['HTTP_HOST'] = 'sentinel.investpro.id'
        
        # Login user
        user = User.objects.first()
        request.user = user
        
        # Call view
        response = sast_report_view(request)
        
        print(f"✅ View status: {response.status_code}")
        if hasattr(response, 'context_data'):
            print(f"📊 Context data: {list(response.context_data.keys())}")
        
    except ImportError as e:
        print(f"❌ Cannot import view: {e}")
        print("💡 Check the actual view name in your views.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_dashboard_view()
