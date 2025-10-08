import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_auth_flow():
    print("🔐 TESTING AUTHENTICATION FLOW")
    print("=" * 50)
    
    client = Client()
    
    # Test tanpa login
    print("1. 🔓 TEST WITHOUT LOGIN:")
    response = client.get('/sast-report/', HTTP_HOST='sentinel.investpro.id')
    print(f"   Status: {response.status_code}")
    if response.status_code == 302:
        print(f"   Redirect to: {response.url}")
    elif response.status_code == 200:
        print("   ⚠️  Accessed without login (check @login_required)")
    
    # Test dengan login
    print("\n2. 🔐 TEST WITH LOGIN:")
    user = User.objects.first()
    if user:
        client.force_login(user)
        response = client.get('/sast-report/', HTTP_HOST='sentinel.investpro.id')
        print(f"   Status: {response.status_code}")
        print(f"   User: {user.username}")
        
        # Check content
        content = response.content.decode('utf-8')
        if 'SAST Security Dashboard' in content:
            print("   ✅ Dashboard content found")
        else:
            print("   ❌ Dashboard content missing")
    else:
        print("   ❌ No users found")

if __name__ == '__main__':
    test_auth_flow()
