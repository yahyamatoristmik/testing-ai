# services/sync_service.py
import requests
from ..models import UserSCMProfile, Repository

def sync_repositories_for_user(user):
    """Sync repositories for a specific user - reusable function"""
    print(f"🔄 Starting sync for user: {user.username}")
    
    scm_profiles = UserSCMProfile.objects.filter(user=user, is_active=True)
    
    if not scm_profiles:
        return {'success': False, 'error': 'No active SCM profiles found', 'synced_count': 0}
    
    total_synced = 0
    errors = []
    
    for scm_profile in scm_profiles:
        try:
            if scm_profile.scm_type == 'github':
                synced = sync_github_repositories_scm(scm_profile)
            elif scm_profile.scm_type == 'gitlab':
                synced = sync_gitlab_repositories_scm(scm_profile)
            elif scm_profile.scm_type == 'bitbucket':
                synced = sync_bitbucket_repositories_scm(scm_profile)
            else:
                continue
            
            if synced > 0:
                total_synced += synced
            else:
                errors.append(f"No repositories synced from {scm_profile.scm_type}")
                
        except Exception as e:
            errors.append(f"Sync failed for {scm_profile.scm_type}: {str(e)}")
    
    if errors and total_synced == 0:
        return {'success': False, 'error': '; '.join(errors), 'synced_count': total_synced}
    elif errors:
        return {'success': True, 'error': '; '.join(errors), 'synced_count': total_synced}
    else:
        return {'success': True, 'synced_count': total_synced, 'error': None}

def sync_github_repositories_scm(scm_profile):
    """Sync GitHub repositories"""
    headers = {
        'Authorization': f'token {scm_profile.access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    base_url = scm_profile.api_url or 'https://api.github.com'
    user_repos_url = f"{base_url}/user/repos?per_page=100&affiliation=owner,collaborator"
    
    try:
        response = requests.get(user_repos_url, headers=headers, timeout=30)
        if response.status_code != 200:
            return 0
            
        repos_data = response.json()
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
            if created:
                synced_count += 1
        
        return synced_count
        
    except Exception:
        return 0

def sync_gitlab_repositories_scm(scm_profile):
    """Sync GitLab repositories"""
    headers = {
        'Private-Token': scm_profile.access_token
    }
    
    base_url = scm_profile.api_url or 'https://gitlab.com/api/v4'
    projects_url = f"{base_url}/projects?membership=true&per_page=100"
    
    try:
        response = requests.get(projects_url, headers=headers, timeout=30)
        if response.status_code != 200:
            return 0
            
        projects = response.json()
        synced_count = 0
        
        for project in projects:
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
                synced_count += 1
        
        return synced_count
        
    except Exception:
        return 0

def sync_bitbucket_repositories_scm(scm_profile):
    """Sync Bitbucket repositories"""
    auth = (scm_profile.username, scm_profile.access_token)
    base_url = scm_profile.api_url or 'https://api.bitbucket.org/2.0'
    workspaces_url = f"{base_url}/workspaces?role=member"
    
    try:
        response = requests.get(workspaces_url, auth=auth, timeout=30)
        if response.status_code != 200:
            return 0
            
        workspaces_data = response.json()
        all_repos = []
        
        for workspace in workspaces_data.get('values', []):
            workspace_slug = workspace['slug']
            repos_url = f"{base_url}/repositories/{workspace_slug}?pagelen=100"
            
            repos_response = requests.get(repos_url, auth=auth, timeout=30)
            if repos_response.status_code == 200:
                repos_data = repos_response.json()
                all_repos.extend(repos_data.get('values', []))
        
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
            if created:
                synced_count += 1
        
        return synced_count
        
    except Exception:
        return 0
