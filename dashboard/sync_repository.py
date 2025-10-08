# sync_repositories.py
import os
import django
import requests
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import UserSCMProfile, Repository
from django.contrib.auth.models import User

def sync_gitlab_repositories():
    user = User.objects.get(username='yoyox')
    scm_profile = UserSCMProfile.objects.get(user=user, scm_type='gitlab')
    
    print(f"🔄 Syncing GitLab repositories for {user.username}...")
    
    headers = {
        'Private-Token': scm_profile.access_token
    }
    
    # GitLab API endpoint untuk get user's projects
    if scm_profile.api_url:
        base_url = scm_profile.api_url.rstrip('/')
    else:
        base_url = 'https://gitlab.com/api/v4'
    
    url = f"{base_url}/projects?membership=true&simple=true&per_page=100"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        projects = response.json()
        print(f"📦 Found {len(projects)} projects in GitLab")
        
        synced_count = 0
        for project in projects:
            repo, created = Repository.objects.get_or_create(
                scm_profile=scm_profile,
                repo_id=str(project['id']),
                defaults={
                    'name': project['name'],
                    'url': project['web_url'],
                    'private': project.get('visibility', 'private') != 'public',
                    'default_branch': project.get('default_branch', 'main'),
                    'description': project.get('description', ''),
                    'is_active': True
                }
            )
            
            if created:
                print(f"✅ Added: {project['name']}")
                synced_count += 1
            else:
                # Update existing repository
                repo.name = project['name']
                repo.url = project['web_url']
                repo.private = project.get('visibility', 'private') != 'public'
                repo.default_branch = project.get('default_branch', 'main')
                repo.is_active = True
                repo.save()
                print(f"🔄 Updated: {project['name']}")
        
        print(f"🎉 Successfully synced {synced_count} repositories")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error syncing repositories: {e}")
        return False

if __name__ == "__main__":
    sync_gitlab_repositories()
