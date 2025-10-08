import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import UserSCMProfile

def test_github_token(token, api_url=None):
    """Test GitHub token validity"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f"{api_url or 'https://api.github.com'}/user"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            return True, f"✅ Valid - User: {user_data.get('login')}"
        else:
            return False, f"❌ Invalid - HTTP {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return False, f"❌ Error: {e}"

def test_gitlab_token(token, api_url=None):
    """Test GitLab token validity"""
    headers = {
        'Private-Token': token
    }
    url = f"{api_url or 'https://gitlab.com/api/v4'}/user"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            return True, f"✅ Valid - User: {user_data.get('username')}"
        else:
            return False, f"❌ Invalid - HTTP {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return False, f"❌ Error: {e}"

def test_bitbucket_token(username, token, api_url=None):
    """Test Bitbucket token validity"""
    auth = (username, token)
    url = f"{api_url or 'https://api.bitbucket.org/2.0'}/user"
    
    try:
        response = requests.get(url, auth=auth, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            return True, f"✅ Valid - User: {user_data.get('username')}"
        else:
            return False, f"❌ Invalid - HTTP {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return False, f"❌ Error: {e}"

def test_all_tokens():
    """Test all SCM tokens in database"""
    print("🔐 Testing SCM Token Validity")
    print("=" * 60)
    
    scm_profiles = UserSCMProfile.objects.filter(is_active=True)
    
    if not scm_profiles:
        print("❌ No active SCM profiles found!")
        return
    
    valid_count = 0
    
    for profile in scm_profiles:
        print(f"\n👤 User: {profile.user.username}")
        print(f"📋 SCM: {profile.scm_type.upper()}")
        print(f"👤 SCM Username: {profile.username}")
        print(f"🔗 API: {profile.api_url or 'Default'}")
        print(f"🔑 Token: {profile.access_token[:10]}...{profile.access_token[-5:] if len(profile.access_token) > 15 else ''}")
        print("-" * 40)
        
        try:
            if profile.scm_type == 'github':
                valid, message = test_github_token(profile.access_token, profile.api_url)
            elif profile.scm_type == 'gitlab':
                valid, message = test_gitlab_token(profile.access_token, profile.api_url)
            elif profile.scm_type == 'bitbucket':
                valid, message = test_bitbucket_token(profile.username, profile.access_token, profile.api_url)
            else:
                message = "❌ Unsupported SCM type"
                valid = False
            
            print(f"Status: {message}")
            if valid:
                valid_count += 1
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 TOKEN VALIDITY SUMMARY:")
    print(f"   Total SCM profiles: {len(scm_profiles)}")
    print(f"   Valid tokens: {valid_count}")
    print(f"   Invalid tokens: {len(scm_profiles) - valid_count}")

if __name__ == "__main__":
    test_all_tokens()
