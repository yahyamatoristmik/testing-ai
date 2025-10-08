import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_browser_fixed():
    print("🌐 TESTING BROWSER RESPONSE (FIXED HOST)")
    print("=" * 50)
    
    client = Client()
    user = User.objects.first()
    
    if not user:
        print("❌ No user found")
        return
    
    # Force login
    client.force_login(user)
    
    # Get dashboard response dengan host yang benar
    response = client.get('/sast-report/', HTTP_HOST='sentinel.investpro.id')
    
    print(f"📊 RESPONSE INFO:")
    print(f"   Status Code: {response.status_code}")
    print(f"   Content Type: {response['Content-Type']}")
    print(f"   Content Length: {len(response.content)} bytes")
    
    # Check for common issues
    content = response.content.decode('utf-8')
    
    print(f"\n🔍 CONTENT ANALYSIS:")
    
    # Check for HTML structure
    if '<!DOCTYPE html>' in content:
        print("   ✅ HTML doctype found")
    else:
        print("   ❌ HTML doctype missing")
    
    if 'Security Dashboard' in content:
        print("   ✅ Dashboard content found")
    else:
        print("   ❌ Dashboard content missing")
    
    # Check for data
    checks = [
        ('Total Scans', 'Total Scans text'),
        ('High Risk', 'High Risk text'), 
        ('Recent Security Scans', 'Recent Scans section'),
        ('completed', 'Scan status'),
    ]
    
    for text, description in checks:
        if text in content:
            print(f"   ✅ {description}: FOUND")
        else:
            print(f"   ❌ {description}: MISSING")
    
    # Check for errors
    if 'error' in content.lower() or 'traceback' in content.lower():
        print("   ⚠️  Errors found in content")
        # Show error snippet
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'error' in line.lower() or 'traceback' in line.lower():
                print(f"      Line {i}: {line.strip()[:100]}")
    
    # Save full response for inspection
    with open('/tmp/browser_response_fixed.html', 'w') as f:
        f.write(content)
    
    print(f"\n💾 Full response saved to: /tmp/browser_response_fixed.html")
    print(f"📁 File size: {len(content)} characters")
    
    # Show preview
    print(f"\n📄 CONTENT PREVIEW (lines 50-70):")
    lines = content.split('\n')[50:70]
    for i, line in enumerate(lines, 50):
        stripped = line.strip()
        if stripped and len(stripped) > 10:
            print(f"   {i}: {stripped[:100]}")

if __name__ == '__main__':
    test_browser_fixed()
