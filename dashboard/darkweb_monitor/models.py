from django.db import models
from django.contrib.auth.models import User

class DarkWebConfig(models.Model):
    is_active = models.BooleanField(default=False)
    # API Keys untuk berbagai services
    hibp_api_key = models.CharField(max_length=255, blank=True, null=True)  # Have I Been Pwned
    dehashed_api_key = models.CharField(max_length=255, blank=True, null=True)  # DeHashed
    dehashed_email = models.CharField(max_length=255, blank=True, null=True)
    breachdirectory_api_key = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DarkWeb Config ({'Active' if self.is_active else 'Inactive'})"

class DarkWebScan(models.Model):
    SCAN_STATUS = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    SCAN_TYPES = [
        ('company', 'Company Domain'),
        ('email', 'Email Address'),
        ('credential', 'Credential Monitoring'),
    ]
    
    target = models.CharField(max_length=255)
    scan_type = models.CharField(max_length=50, choices=SCAN_TYPES, default='company')
    status = models.CharField(max_length=20, choices=SCAN_STATUS, default='pending')
    results = models.JSONField(null=True, blank=True)
    risk_score = models.IntegerField(default=0)  # 0-100
    error_message = models.TextField(blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"DarkWeb Scan: {self.target} - {self.status}"

class DarkWebFinding(models.Model):
    RISK_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    SOURCES = [
        ('hibp', 'Have I Been Pwned'),
        ('dehashed', 'DeHashed'),
        ('breachdirectory', 'BreachDirectory'),
        ('public_breaches', 'Public Breaches'),
    ]
    
    scan = models.ForeignKey(DarkWebScan, on_delete=models.CASCADE, related_name='findings')
    source = models.CharField(max_length=50, choices=SOURCES)
    finding_type = models.CharField(max_length=100)
    description = models.TextField()
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='low')
    data_points = models.IntegerField(default=0)
    breach_date = models.DateField(null=True, blank=True)
    raw_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} - {self.finding_type} - {self.risk_level}"

class UserDarkWebPermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_access_darkweb = models.BooleanField(default=False)
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='darkweb_grants')

    def __str__(self):
        return f"{self.user.username} - {'Has Access' if self.can_access_darkweb else 'No Access'}"
