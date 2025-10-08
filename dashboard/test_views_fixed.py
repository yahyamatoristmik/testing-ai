import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
import sast_report.views as views

def test_views_fixed():
    print("🧪 TESTING FIXED VIEWS")
    print("=" * 50)
    
    factory = RequestFactory()
    user = User.objects.first()
    
    # Test dashboard view
    print("\n1. 📊 TESTING DASHBOARD VIEW (FIXED)")
    try:
        request = factory.get('/sast-report/')
        request.user = user
        response = views.dashboard(request)
        
        print(f"   Status: {response.status_code}")
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"   ✅ Context keys: {list(context.keys())}")
            
            # Check important data
            for key in ['scan_stats', 'vulnerability_stats', 'recent_scans']:
                if key in context:
                    data = context[key]
                    if key == 'scan_stats':
                        print(f"   📈 Scan stats: {data}")
                    elif key == 'vulnerability_stats':
                        print(f"   ⚠️  Vuln stats: {data}")
                    elif key == 'recent_scans':
                        count = data.count() if hasattr(data, 'count') else len(data)
                        print(f"   🔍 Recent scans: {count}")
                else:
                    print(f"   ❌ Missing: {key}")
        else:
            print("   ❌ No context data")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test scan jobs view
    print("\n2. 📋 TESTING SCAN JOBS VIEW (FIXED)")
    try:
        request = factory.get('/sast-report/scan-jobs/')
        request.user = user
        response = views.scan_jobs(request)
        
        print(f"   Status: {response.status_code}")
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"   ✅ Context keys: {list(context.keys())}")
            if 'scan_jobs' in context:
                scan_jobs = context['scan_jobs']
                print(f"   🔍 Scan jobs count: {scan_jobs.count()}")
        else:
            print("   ❌ No context data")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == '__main__':
    test_views_fixed()
