from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserSCMProfile(models.Model):
    SCM_TYPE_CHOICES = [
        ('github', 'GitHub'),
        ('gitlab', 'GitLab'),
        ('bitbucket', 'Bitbucket'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    scm_type = models.CharField(max_length=20, choices=SCM_TYPE_CHOICES, default='github')
    access_token = models.TextField(blank=True, default='')
    username = models.CharField(max_length=100, blank=True, default='')
    api_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.scm_type}"

class Repository(models.Model):
    scm_profile = models.ForeignKey(UserSCMProfile, on_delete=models.CASCADE)
    repo_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200, default='Unnamed Repository')
    url = models.URLField()
    private = models.BooleanField(default=False)
    default_branch = models.CharField(max_length=100, default='main')
    last_sync = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('scm_profile', 'repo_id')
    
    def __str__(self):
        return self.name

class ScanJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100, default='main')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    triggered_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    log = models.TextField(blank=True, default='')
    findings_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Scan {self.repository.name} - {self.status}"

class VulnerabilityReport(models.Model):
    SEVERITY_CHOICES = [
        ('CRITICAL', 'Critical'),
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
        ('INFO', 'Info'),
    ]
    
    scan_job = models.ForeignKey(ScanJob, on_delete=models.CASCADE)
    rule_id = models.CharField(max_length=200, default='unknown')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='MEDIUM')
    file_path = models.CharField(max_length=500)
    line_number = models.IntegerField(default=0)
    message = models.TextField()
    description = models.TextField(blank=True, default='')
    recommendation = models.TextField(blank=True, default='')
    metadata = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.rule_id} - {self.file_path}:{self.line_number}"
