# docker_health.py
import docker
import logging

logger = logging.getLogger(__name__)

def check_semgrep_image():
    """Check if Semgrep image is available"""
    try:
        client = docker.from_env()
        images = client.images.list()
        semgrep_images = [img for img in images if any('semgrep' in tag for tag in img.tags)]
        return len(semgrep_images) > 0
    except Exception as e:
        logger.error(f"Docker health check failed: {e}")
        return False

def pull_semgrep_image():
    """Pull the latest Semgrep image"""
    try:
        client = docker.from_env()
        client.images.pull('returntocorp/semgrep:latest')
        return True
    except Exception as e:
        logger.error(f"Failed to pull Semgrep image: {e}")
        return False
