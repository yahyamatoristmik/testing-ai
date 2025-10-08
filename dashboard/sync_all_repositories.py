import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import UserSCMProfile, Repository
from django.contrib.auth.models import User

def sync_github_repositories(scm_profile):
    """Sync repositories from GitHub"""
    print(f"🔄 Syncing GitHub repositories for {scm_profile.username}...")
    
    headers = {
        'Authorization': f'token {scm_profile.access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    base_url = scm_profile.api_url or 'https://api.github.com'
    
    # Get user repos
    user_repos_url = f"{base_url}/user/repos?per_page=100&affiliation=owner,collaborator"
    
    try:
        response = requests.get(user_repos_url, headers=headers, timeout=30)
        response.raise_for_status()
        repos_data = response.json()
        
        print(f"📦 Found {len(repos_data)} repositories on GitHub")
        
        synced_count = 0
        for repo_data in repos_data:
            repo, created = Repository.objects.update_or_create(
                scm_profile=scm_profile,
                repo_id=str(repo_data['id']),
                defaults={
                    'name': repo_data['name'],
                    'url': repo_data['html_url'],
                    'private': repo_data['private'],
                    'default_branch': repo_data.get('default_branch', 'main'),
                    'description': repo_data.get('description', '')[:500],
                    'is_active': True
                }
            )
            
            status = "✅ ADDED" if created else "🔄 UPDATED"
            print(f"{status}: {repo_data['name']} ({'private' if repo_data['private'] else 'public'})")
            synced_count += 1
        
        print(f"🎉 Successfully synced {synced_count} GitHub repositories")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error syncing GitHub repositories: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"HTTP {e.response.status_code}: {e.response.text}")
        return False

def sync_gitlab_repositories(scm_profile):
    """Sync repositories from GitLab"""
    print(f"🔄 Syncing GitLab repositories for {scm_profile.username}...")
    
    headers = {
        'Private-Token': scm_profile.access_token
    }
    
    base_url = scm_profile.api_url or 'https://gitlab.com/api/v4'
    
    # Get projects where user is member
    projects_url = f"{base_url}/projects?membership=true&per_page=100"
    
    try:
        print(f"📡 Calling GitLab API: {projects_url}")
        response = requests.get(projects_url, headers=headers, timeout=30)
        
        # Check for 401 Unauthorized
        if response.status_code == 401:
            print(f"❌ GitLab API returned 401 Unauthorized")
            print(f"   Please check your access token for user: {scm_profile.username}")
            return False
        elif response.status_code == 403:
            print(f"❌ GitLab API returned 403 Forbidden")
            print(f"   Token might have insufficient permissions")
            return False
        
        response.raise_for_status()
        
        # Debug: Print response snippet
        print(f"📄 Response status: {response.status_code}")
        print(f"📄 Response length: {len(response.text)}")
        
        projects = response.json()
        
        # Check if response is a list
        if not isinstance(projects, list):
            print(f"❌ Unexpected response format from GitLab API")
            print(f"   Response type: {type(projects)}")
            print(f"   Response keys: {projects.keys() if hasattr(projects, 'keys') else 'N/A'}")
            return False
        
        print(f"📦 Found {len(projects)} projects on GitLab")
        
        synced_count = 0
        for project in projects:
            # Safe access to project data
            project_id = project.get('id')
            project_name = project.get('name', 'Unknown')
            web_url = project.get('web_url', '')
            visibility = project.get('visibility', 'private')
            default_branch = project.get('default_branch', 'main')
            description = project.get('description', '')[:500] if project.get('description') else ''
            
            if not project_id:
                print(f"⚠️  Skipping project without ID: {project_name}")
                continue
            
            try:
                repo, created = Repository.objects.update_or_create(
                    scm_profile=scm_profile,
                    repo_id=str(project_id),
                    defaults={
                        'name': project_name,
                        'url': web_url,
                        'private': visibility != 'public',
                        'default_branch': default_branch,
                        'description': description,
                        'is_active': True
                    }
                )
                
                status = "✅ ADDED" if created else "🔄 UPDATED"
                print(f"{status}: {project_name} ({visibility})")
                synced_count += 1
                
            except Exception as e:
                print(f"❌ Error saving repository {project_name}: {e}")
                continue
        
        print(f"🎉 Successfully synced {synced_count} GitLab repositories")
        return synced_count > 0
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error syncing GitLab repositories: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"HTTP {e.response.status_code}: {e.response.text[:200]}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in GitLab sync: {e}")
        return False


def sync_bitbucket_repositories(scm_profile):
    """Sync repositories from Bitbucket"""
    print(f"🔄 Syncing Bitbucket repositories for {scm_profile.username}...")
    
    auth = (scm_profile.username, scm_profile.access_token)
    base_url = scm_profile.api_url or 'https://api.bitbucket.org/2.0'
    
    # Get user workspaces first
    workspaces_url = f"{base_url}/workspaces?role=member"
    
    try:
        response = requests.get(workspaces_url, auth=auth, timeout=30)
        response.raise_for_status()
        workspaces_data = response.json()
        
        all_repos = []
        
        # Get repositories from each workspace
        for workspace in workspaces_data.get('values', []):
            workspace_slug = workspace['slug']
            repos_url = f"{base_url}/repositories/{workspace_slug}?pagelen=100"
            
            repos_response = requests.get(repos_url, auth=auth, timeout=30)
            repos_response.raise_for_status()
            repos_data = repos_response.json()
            
            all_repos.extend(repos_data.get('values', []))
        
        print(f"📦 Found {len(all_repos)} repositories on Bitbucket")
        
        synced_count = 0
        for repo_data in all_repos:
            repo, created = Repository.objects.update_or_create(
                scm_profile=scm_profile,
                repo_id=repo_data['uuid'],
                defaults={
                    'name': repo_data['name'],
                    'url': repo_data['links']['html']['href'],
                    'private': repo_data.get('is_private', True),
                    'default_branch': repo_data.get('mainbranch', {}).get('name', 'main'),
                    'description': repo_data.get('description', '')[:500],
                    'is_active': True
                }
            )
            
            status = "✅ ADDED" if created else "🔄 UPDATED"
            visibility = 'private' if repo_data.get('is_private', True) else 'public'
            print(f"{status}: {repo_data['name']} ({visibility})")
            synced_count += 1
        
        print(f"🎉 Successfully synced {synced_count} Bitbucket repositories")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error syncing Bitbucket repositories: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"HTTP {e.response.status_code}: {e.response.text}")
        return False

def sync_all_users_repositories():
    """Sync repositories for all users with SCM profiles"""
    print("🚀 Starting repository sync for all users...")
    print("=" * 60)
    
    # Get all active SCM profiles
    scm_profiles = UserSCMProfile.objects.filter(is_active=True)
    
    if not scm_profiles:
        print("❌ No active SCM profiles found!")
        print("Please configure SCM integration first in the web interface.")
        return
    
    total_synced = 0
    
    for scm_profile in scm_profiles:
        print(f"\n👤 User: {scm_profile.user.username}")
        print(f"📋 SCM: {scm_profile.scm_type.upper()}")
        print(f"🔗 API: {scm_profile.api_url or 'Default'}")
        print("-" * 40)
        
        try:
            if scm_profile.scm_type == 'github':
                success = sync_github_repositories(scm_profile)
            elif scm_profile.scm_type == 'gitlab':
                success = sync_gitlab_repositories(scm_profile)
            elif scm_profile.scm_type == 'bitbucket':
                success = sync_bitbucket_repositories(scm_profile)
            else:
                print(f"❌ Unsupported SCM type: {scm_profile.scm_type}")
                continue
            
            if success:
                total_synced += 1
                
        except Exception as e:
            print(f"❌ Unexpected error for {scm_profile.user.username}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print(f"📊 SYNC SUMMARY:")
    print(f"   Total SCM profiles processed: {len(scm_profiles)}")
    print(f"   Successfully synced: {total_synced}")
    
    # Show repository statistics
    from django.db.models import Count
    repo_stats = Repository.objects.values('scm_profile__scm_type').annotate(
        count=Count('id')
    ).order_by('scm_profile__scm_type')
    
    print(f"\n📁 REPOSITORY STATISTICS:")
    for stat in repo_stats:
        scm_type = stat['scm_profile__scm_type']
        count = stat['count']
        print(f"   {scm_type.upper()}: {count} repositories")

def sync_specific_user(username):
    """Sync repositories for a specific user"""
    try:
        user = User.objects.get(username=username)
        scm_profiles = UserSCMProfile.objects.filter(user=user, is_active=True)
        
        if not scm_profiles:
            print(f"❌ No active SCM profiles found for user: {username}")
            return
        
        print(f"🚀 Syncing repositories for user: {username}")
        
        for scm_profile in scm_profiles:
            print(f"\n📋 SCM: {scm_profile.scm_type.upper()}")
            print("-" * 40)
            
            if scm_profile.scm_type == 'github':
                sync_github_repositories(scm_profile)
            elif scm_profile.scm_type == 'gitlab':
                sync_gitlab_repositories(scm_profile)
            elif scm_profile.scm_type == 'bitbucket':
                sync_bitbucket_repositories(scm_profile)
                
    except User.DoesNotExist:
        print(f"❌ User not found: {username}")
        print("\nAvailable users with SCM profiles:")
        users_with_scm = User.objects.filter(
            userscmprofile__is_active=True
        ).distinct()
        
        for user in users_with_scm:
            scm_types = UserSCMProfile.objects.filter(
                user=user, is_active=True
            ).values_list('scm_type', flat=True)
            print(f"  - {user.username} ({', '.join(scm_types)})")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Sync specific user: python sync_all_repositories.py username
        username = sys.argv[1]
        sync_specific_user(username)
    else:
        # Sync all users
        sync_all_users_repositories()
