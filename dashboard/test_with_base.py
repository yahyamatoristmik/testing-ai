import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.template.loader import render_to_string
from sast_report.models import ScanJob, VulnerabilityReport, Repository

def test_with_base():
    print("🧪 TESTING WITH BASE TEMPLATE")
    print("=" * 50)
    
    context = {
        'scan_stats': {
            'total': ScanJob.objects.count(),
            'completed': ScanJob.objects.filter(status='completed').count(),
            'running': ScanJob.objects.filter(status='running').count(),
        },
        'vulnerability_stats': {
            'total': VulnerabilityReport.objects.count(),
            'high': VulnerabilityReport.objects.filter(severity='HIGH').count(),
            'medium': VulnerabilityReport.objects.filter(severity='MEDIUM').count(),
        },
        'recent_scans': ScanJob.objects.all().select_related('repository').order_by('-id')[:5],
    }
    
    try:
        html = render_to_string('sast_report/dashboard.html', context)
        print("✅ DASHBOARD WITH BASE TEMPLATE RENDERED!")
        print(f"📏 HTML length: {len(html)} characters")
        
        # Check critical elements
        checks = [
            ('SAST Security', 'Page title'),
            ('Security Dashboard', 'Dashboard header'),
            (str(context['scan_stats']['total']), 'Total scans number'),
            (str(context['vulnerability_stats']['high']), 'High vulnerabilities number'),
        ]
        
        print("\n🔍 CHECKING CRITICAL ELEMENTS:")
        for text, description in checks:
            if text in html:
                print(f"   ✅ {description}: FOUND")
            else:
                print(f"   ❌ {description}: NOT FOUND")
                
        # Save to file for inspection
        with open('/tmp/dashboard_output.html', 'w') as f:
            f.write(html)
        print(f"💾 Output saved to: /tmp/dashboard_output.html")
        
    except Exception as e:
        print(f"❌ Render error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_with_base()
