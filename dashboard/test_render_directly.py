import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.template.loader import render_to_string
from django.contrib.auth.models import User
from sast_report.models import ScanJob, VulnerabilityReport, Repository

def test_render_directly():
    print("🧪 TESTING RENDER DIRECTLY")
    print("=" * 50)
    
    # Create context manually
    context = {
        'scan_stats': {
            'total': ScanJob.objects.count(),
            'completed': ScanJob.objects.filter(status='completed').count(),
            'running': ScanJob.objects.filter(status='running').count(),
            'pending': ScanJob.objects.filter(status='pending').count(),
        },
        'vulnerability_stats': {
            'total': VulnerabilityReport.objects.count(),
            'high': VulnerabilityReport.objects.filter(severity='HIGH').count(),
            'medium': VulnerabilityReport.objects.filter(severity='MEDIUM').count(),
        },
        'recent_scans': ScanJob.objects.all().select_related('repository').order_by('-id')[:5],
        'repositories': Repository.objects.all()[:3],
    }
    
    print("📊 CONTEXT DATA:")
    print(f"   scan_stats: {context['scan_stats']}")
    print(f"   vulnerability_stats: {context['vulnerability_stats']}")
    print(f"   recent_scans: {context['recent_scans'].count()} scans")
    print(f"   repositories: {context['repositories'].count()} repos")
    
    # Try to render template
    try:
        html = render_to_string('sast_report/dashboard.html', context)
        print("✅ TEMPLATE RENDERED SUCCESSFULLY!")
        print(f"📏 HTML length: {len(html)} characters")
        
        # Check if important data appears in HTML
        checks = [
            (str(context['scan_stats']['total']), 'Total Scans'),
            (str(context['vulnerability_stats']['high']), 'High Vulnerabilities'),
            (str(context['recent_scans'].count()), 'Recent Scans Count')
        ]
        
        print("\n🔍 CHECKING RENDERED CONTENT:")
        for text, description in checks:
            if text in html:
                print(f"   ✅ {description}: FOUND")
            else:
                print(f"   ❌ {description}: NOT FOUND")
                
    except Exception as e:
        print(f"❌ Template render error: {e}")

if __name__ == '__main__':
    test_render_directly()
