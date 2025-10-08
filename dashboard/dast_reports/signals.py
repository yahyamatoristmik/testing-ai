from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserLoginLog
import logging

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Signal untuk mencatat successful login
    """
    try:
        login_log = UserLoginLog.log_login(user, request, success=True)
        if login_log:
            logger.info(f"User {user.username} logged in successfully from IP: {login_log.ip_address}")
        else:
            logger.error(f"Failed to log login for {user.username}")
    except Exception as e:
        logger.error(f"Error logging successful login for {user.username}: {str(e)}")

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """
    Signal untuk mencatat failed login attempt
    """
    try:
        username = credentials.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                login_log = UserLoginLog.log_login(user, request, success=False)
                if login_log:
                    logger.warning(f"Failed login attempt for user {username} from IP: {login_log.ip_address}")
            except User.DoesNotExist:
                # Untuk user yang tidak ditemukan, buat log tanpa user
                ip_address = UserLoginLog.get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
                
                login_log = UserLoginLog.objects.create(
                    user=None,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    success=False,
                    name=f"Failed login - {username} - Unknown user"
                )
                logger.warning(f"Failed login attempt for non-existent user {username} from IP: {ip_address}")
                
    except Exception as e:
        logger.error(f"Error logging failed login attempt: {str(e)}")
