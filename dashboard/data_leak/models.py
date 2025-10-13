from django.db import models
from django.contrib.auth.models import User

class DataLeakConfig(models.Model):
    is_active = models.BooleanField(default=False)
    api_key = models.CharField(max_length=255, default='your-api-key-here')
    api_url = models.CharField(max_length=255, default='https://api.whiteintel.io/v1/scan')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Data Leak Config ({'Active' if self.is_active else 'Inactive'})"

class DataLeakScan(models.Model):
    SCAN_STATUS = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    target = models.CharField(max_length=255)
    scan_type = models.CharField(max_length=50, default='domain')
    status = models.CharField(max_length=20, choices=SCAN_STATUS, default='pending')
    results = models.TextField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Scan: {self.target} - {self.status}"

class UserDataLeakPermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_access_data_leak = models.BooleanField(default=False)
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_leak_grants')

    def __str__(self):
        return f"{self.user.username} - {'Has Access' if self.can_access_data_leak else 'No Access'}"
