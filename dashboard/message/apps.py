# ==========================================
# STEP 6: dashboard/message/apps.py
# ==========================================
from django.apps import AppConfig

class MessageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message'
    verbose_name = 'Contact Messages'
