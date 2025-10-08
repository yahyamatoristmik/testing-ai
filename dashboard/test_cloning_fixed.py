import os
import django
import tempfile
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import Repository, UserSCMProfile
from django.contrib.auth.models import User

def test_cloning_fixed():
    print("🧪 TESTING REPOSITORY CLONING - FIXED VERSION")
    
    # Gunakan user admin
    user = User.objects.get(username='admin')
    scm_profile = UserSCMProfile.objects.get(user=user, scm_type='gitlab')
    repository = Repository.objects.filter(scm_profile=scm_profile).first()
    
    if not repository:
        print("❌ No repository found")
        return
    
    print(f"📦 Testing clone for: {repository.name}")
    print(f"🔗 URL: {repository.url}")
    print(f"🔐 Private: {repository.private}")
    print(f"👤 SCM User: {scm_profile.username}")
    print(f"🏷️ SCM Type: {scm_profile.scm_type}")
    print(f"🔑 Token preview: {scm_profile.access_token[:10]}...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = os.path.join(temp_dir, 'repo')
        print(f"📁 Temp dir: {temp_dir}")
        
        # Test 1: Coba clone dengan authentication (seperti di tasks.py)
        print("\n1. Testing authenticated clone (tasks.py method)...")
        try:
            # Sama seperti di clone_gitlab_repository function
            if repository.private and scm_profile.access_token:
                clone_url = f"https://oauth2:{scm_profile.access_token}@gitlab.com/{scm_profile.username}/{repository.name}.git"
            else:
                clone_url = repository.url
            
            print(f"🔑 Clone URL: {clone_url}")
            
            result = subprocess.run([
                'git', 'clone', '--depth', '1', '--branch', repository.default_branch, clone_url, repo_dir
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ Authenticated clone SUCCESS")
                print(f"📂 Contents: {os.listdir(repo_dir)}")
                return True
            else:
                print(f"❌ Authenticated clone FAILED: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Authenticated clone ERROR: {e}")
        
        # Test 2: Coba alternative method (public URL)
        print("\n2. Testing alternative clone (public URL)...")
        try:
            result = subprocess.run([
                'git', 'clone', '--depth', '1', repository.url, repo_dir
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ Alternative clone SUCCESS")
                print(f"📂 Contents: {os.listdir(repo_dir)}")
                return True
            else:
                print(f"❌ Alternative clone FAILED: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Alternative clone ERROR: {e}")
    
    return False

if __name__ == "__main__":
    success = test_cloning_fixed()
    print(f"\n🎯 FINAL RESULT: {'SUCCESS' if success else 'FAILED'}")
