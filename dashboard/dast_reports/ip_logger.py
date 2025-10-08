import os
import datetime
from django.conf import settings

def log_user_login(user, ip_address, success=True):
    """
    Log login activity ke file text (tanpa database)
    """
    log_dir = os.path.join(settings.BASE_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'user_logins.log')
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    
    log_entry = f"[{timestamp}] {status} - User: {user.username} - IP: {ip_address}\n"
    
    try:
        with open(log_file, 'a') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to login log: {e}")

def get_recent_logins(days=7):
    """
    Baca log login recent (untuk admin view)
    """
    log_file = os.path.join(settings.BASE_DIR, 'logs', 'user_logins.log')
    
    if not os.path.exists(log_file):
        return []
    
    recent_logs = []
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
    
    try:
        with open(log_file, 'r') as f:
            for line in f.readlines()[-100:]:  # Ambil 100 line terakhir
                if line.strip():
                    recent_logs.append(line.strip())
    except Exception as e:
        print(f"Error reading login log: {e}")
    
    return recent_logs[-20:]  # Return 20 log terakhir
