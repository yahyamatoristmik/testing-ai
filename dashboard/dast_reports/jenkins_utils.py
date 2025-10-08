import jenkins
import requests
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

class JenkinsZAPTrigger:
    def __init__(self):
        self.config = getattr(settings, 'JENKINS_CONFIG', {})
        self.server = None

        try:
            self.server = jenkins.Jenkins(
                self.config['BASE_URL'],
                username=self.config['USERNAME'],
                password=self.config['API_TOKEN']
            )
            # Test connection
            self.server.get_whoami()
            logger.info("Jenkins connected successfully")
        except Exception as e:
            logger.error(f"Jenkins connection failed: {e}")
            self.server = None

    def trigger_zap_scan(self, target_url, scan_name=None):
        """Trigger ZAP scan job di Jenkins dan return build number"""
        try:
            # Parameters untuk Jenkins job
            params = {
                'TARGET_URL': target_url,
                'SCAN_NAME': scan_name or f"Scan-{target_url}"
            }

            # Get next build number before triggering
            job_info = self.server.get_job_info(self.config['ZAP_JOB_NAME'])
            next_build_number = job_info['nextBuildNumber']
            
            # Trigger Jenkins job
            self.server.build_job(
                self.config['ZAP_JOB_NAME'],
                parameters=params
            )
            
            # Return next build number (will be assigned to this build)
            return True, "Scan triggered successfully", next_build_number

        except jenkins.JenkinsException as e:
            return False, f"Jenkins error: {str(e)}", None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None

# Alternative menggunakan REST API langsung
def trigger_zap_scan_via_rest(target_url, scan_name=None):
    """Alternative: Trigger via REST API"""
    try:
        jenkins_url = f"{settings.JENKINS_CONFIG['BASE_URL']}/job/{settings.JENKINS_CONFIG['ZAP_JOB_NAME']}/buildWithParameters"

        params = {
            'token': settings.JENKINS_CONFIG['ZAP_JOB_TOKEN'],
            'TARGET_URL': target_url,
            'SCAN_NAME': scan_name or f"Scan-{target_url}"
        }

        response = requests.post(
            jenkins_url,
            data=params,
            auth=(
                settings.JENKINS_CONFIG['USERNAME'],
                settings.JENKINS_CONFIG['API_TOKEN']
            )
        )

        if response.status_code in [200, 201]:
            # Get the next build number
            job_info_url = f"{settings.JENKINS_CONFIG['BASE_URL']}/job/{settings.JENKINS_CONFIG['ZAP_JOB_NAME']}/api/json"
            job_response = requests.get(
                job_info_url,
                auth=(
                    settings.JENKINS_CONFIG['USERNAME'],
                    settings.JENKINS_CONFIG['API_TOKEN']
                )
            )
            
            if job_response.status_code == 200:
                job_data = job_response.json()
                build_number = job_data['nextBuildNumber']
                return True, "Scan triggered successfully", build_number
            else:
                return True, "Scan triggered successfully (build number unknown)", None
        else:
            return False, f"HTTP Error: {response.status_code}", None

    except Exception as e:
        return False, f"Error: {str(e)}", None
