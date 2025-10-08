import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import UserSCMProfile, Repository
from django.contrib.auth.models import User

def sync_gitlab_repositories():
    print("🔄 Syncing GitLab repositories...")
    
    # Get user yoyox
    user = User.objects.get(username='yoyox')
    scm_profile = UserSCMProfile.objects.get(user=user, scm_type='gitlab')
    
    print(f"User: {user.username}")
    print(f"SCM: {scm_profile.scm_type}")
    print(f"API URL: {scm_profile.api_url}")
    print(f"Token: {scm_profile.access_token[:10]}...")
    
    headers = {
        'Private-Token': scm_profile.access_token
    }
    
    # GitLab API endpoint
    base_url = scm_profile.api_url or 'https://gitlab.com/api/v4'
    url = f"{base_url}/projects?membership=true&per_page=100"
    
    try:
        print(f"📡 Calling GitLab API: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        projects = response.json()
        print(f"📦 Found {len(projects)} projects in GitLab")
        
        for project in projects:
            print(f"Processing: {project['name']} (ID: {project['id']})")
            
            repo, created = Repository.objects.update_or_create(
                scm_profile=scm_profile,
                repo_id=str(project['id']),
                defaults={
                    'name': project['name'],
                    'url': project['web_url'],
                    'private': project.get('visibility', 'private') != 'public',
                    'default_branch': project.get('default_branch', 'main'),
                    'description': project.get('description', '')[:500],
                    'is_active': True
                }
            )
            
            if created:
                print(f"✅ ADDED: {project['name']}")
            else:
                print(f"🔄 UPDATED: {project['name']}")
        
        print(f"🎉 Successfully synced {len(projects)} repositories")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error syncing repositories: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"HTTP {e.response.status_code}: {e.response.text}")
        return False

if __name__ == "__main__":
    sync_gitlab_repositories()
