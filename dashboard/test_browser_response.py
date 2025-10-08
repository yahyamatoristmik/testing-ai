import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_browser_response():
    print("🌐 TESTING BROWSER RESPONSE")
    print("=" * 50)
    
    client = Client()
    user = User.objects.first()
    
    if not user:
        print("❌ No user found")
        return
    
    # Force login
    client.force_login(user)
    
    # Get dashboard response
    response = client.get('/sast-report/')
    
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
    
    if '<html' in content:
        print("   ✅ HTML tag found") 
    else:
        print("   ❌ HTML tag missing")
    
    if '<body' in content:
        print("   ✅ Body tag found")
    else:
        print("   ❌ Body tag missing")
    
    # Check for data
    if 'Total Scans' in content:
        print("   ✅ 'Total Scans' text found")
    else:
        print("   ❌ 'Total Scans' text missing")
    
    # Check for errors
    if 'error' in content.lower():
        print("   ⚠️  Error text found in content")
    
    if 'traceback' in content.lower():
        print("   ⚠️  Traceback found in content")
    
    # Save full response for inspection
    with open('/tmp/full_browser_response.html', 'w') as f:
        f.write(content)
    
    print(f"\n💾 Full response saved to: /tmp/full_browser_response.html")
    print(f"📁 File size: {len(content)} characters")
    
    # Show first few lines
    print(f"\n📄 FIRST 10 LINES:")
    lines = content.split('\n')[:10]
    for i, line in enumerate(lines):
        print(f"   {i+1}: {line.strip()[:100]}")

if __name__ == '__main__':
    test_browser_response()
