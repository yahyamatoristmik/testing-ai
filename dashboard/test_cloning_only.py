import os
import django
import tempfile
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import Repository, UserSCMProfile
from django.contrib.auth.models import User
from sast_report.tasks import clone_gitlab_repository, try_alternative_clone

def test_cloning_function():
    print("🧪 TESTING CLONING FUNCTION FROM TASKS.PY")
    
    user = User.objects.get(username='admin')
    scm_profile = UserSCMProfile.objects.get(user=user, scm_type='gitlab')
    repository = Repository.objects.filter(scm_profile=scm_profile).first()
    
    if not repository:
        print("❌ No repository found")
        return
    
    print(f"📦 Testing repository: {repository.name}")
    print(f"🔗 URL: {repository.url}")
    print(f"🔐 Private: {repository.private}")
    print(f"👤 Username: {scm_profile.username}")
    print(f"🏷️ Default branch: {repository.default_branch}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = os.path.join(temp_dir, 'repo')
        
        print(f"\n📁 Temp directory: {temp_dir}")
        
        # Test 1: Clone menggunakan function dari tasks.py
        print("\n1. 🔄 TESTING CLONE_GITLAB_REPOSITORY FUNCTION...")
        success = clone_gitlab_repository(scm_profile, repository, repo_dir)
        
        if success:
            print("✅ clone_gitlab_repository SUCCESS")
            print(f"📂 Contents: {os.listdir(repo_dir)}")
        else:
            print("❌ clone_gitlab_repository FAILED")
            
            # Test 2: Manual clone untuk comparison
            print("\n2. 🔄 TESTING MANUAL CLONE FOR COMPARISON...")
            try:
                manual_cmd = [
                    'git', 'clone', '--depth', '1', 
                    '--branch', repository.default_branch,
                    repository.url, 
                    os.path.join(temp_dir, 'repo_manual')
                ]
                
                print(f"🔧 Manual command: {' '.join(manual_cmd)}")
                
                result = subprocess.run(
                    manual_cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    print("✅ Manual clone SUCCESS")
                    print("❌ Why does manual work but function fails?")
                else:
                    print(f"❌ Manual clone also FAILED: {result.stderr}")
                    
            except Exception as e:
                print(f"❌ Manual clone error: {e}")

if __name__ == "__main__":
    test_cloning_function()
