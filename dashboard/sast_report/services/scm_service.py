import requests
import logging

logger = logging.getLogger(__name__)

class SCMService:
    def __init__(self, scm_profile):
        self.scm_profile = scm_profile
        self.token = scm_profile.token
        self.scm_type = scm_profile.scm_type
        
    def test_connection(self):
        """Test koneksi ke SCM - Simple dan Stabil"""
        try:
            if self.scm_type == 'github':
                headers = {'Authorization': f'token {self.token}'}
                response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
                if response.status_code == 200:
                    user_data = response.json()
                    return True, user_data
                else:
                    return False, f"GitHub API Error: {response.status_code}"
                    
            elif self.scm_type == 'gitlab':
                headers = {'PRIVATE-TOKEN': self.token}
                response = requests.get('https://gitlab.com/api/v4/user', headers=headers, timeout=10)
                if response.status_code == 200:
                    user_data = response.json()
                    return True, user_data
                else:
                    return False, f"GitLab API Error: {response.status_code}"
                    
            elif self.scm_type == 'bitbucket':
                headers = {'Authorization': f'Bearer {self.token}'}
                response = requests.get('https://api.bitbucket.org/2.0/user', headers=headers, timeout=10)
                if response.status_code == 200:
                    user_data = response.json()
                    return True, user_data
                else:
                    return False, f"Bitbucket API Error: {response.status_code}"
                    
        except requests.exceptions.Timeout:
            return False, "Connection timeout after 10 seconds"
        except requests.exceptions.ConnectionError:
            return False, "Connection error - check your internet"
        except Exception as e:
            logger.error(f"SCM connection test failed: {e}")
            return False, f"Unexpected error: {str(e)}"
        
        return False, "Unsupported SCM type"

    def get_repositories_simple(self):
        """Get repositories sederhana untuk start"""
        try:
            # Untuk awal, return sample repository
            return [{
                'repo_id': '1',
                'name': 'Sample Project',
                'url': f'https://{self.scm_type}.com/user/sample',
                'default_branch': 'main',
                'private': False
            }]
        except Exception as e:
            logger.error(f"Failed to get repositories: {e}")
            return []
