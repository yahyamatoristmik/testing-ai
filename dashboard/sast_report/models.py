from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class SCMProfile(models.Model):
    SCM_TYPES = (
        ('github', 'GitHub'),
        ('gitlab', 'GitLab'),
        ('bitbucket', 'Bitbucket'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scm_type = models.CharField(max_length=20, choices=SCM_TYPES, default='github')
    token = models.CharField(max_length=255, default='')
    username = models.CharField(max_length=100, blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.scm_type}"

class Repository(models.Model):
    scm_profile = models.ForeignKey(SCMProfile, on_delete=models.CASCADE)
    repo_id = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=200, default='Repository')
    url = models.URLField(default='')
    default_branch = models.CharField(max_length=100, default='main')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ScanJob(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    branch = models.CharField(max_length=100, default='main')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    scan_log = models.TextField(blank=True, default='')
    error_message = models.TextField(blank=True, default='')
    total_findings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Scan {self.repository.name} - {self.status}"

    @property
    def duration(self):
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def get_duration_display(self):
        if self.duration:
            return f"{self.duration:.1f}s"
        return "N/A"

class Finding(models.Model):
    SEVERITY_CHOICES = (
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('info', 'Info'),
    )
    
    scan_job = models.ForeignKey(ScanJob, on_delete=models.CASCADE, related_name='findings')
    rule_id = models.CharField(max_length=100, default='')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    file_path = models.CharField(max_length=500, default='')
    line_number = models.IntegerField(default=0)
    message = models.TextField(default='')
    description = models.TextField(blank=True, default='')
    code_snippet = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-severity', 'file_path']

    def __str__(self):
        return f"{self.rule_id} - {self.file_path}:{self.line_number}"


class SASTPermission:
    """Custom permissions untuk SAST Report"""
    
    @classmethod
    def create_sast_permissions(cls):
        """Buat custom permissions untuk SAST"""
        content_type = ContentType.objects.get_for_model(SCMProfile)
        
        permissions = [
            ('can_view_sast', 'Can view SAST dashboard'),
            ('can_manage_scm', 'Can manage SCM profiles'),
            ('can_run_scan', 'Can run security scans'),
            ('can_view_reports', 'Can view scan reports'),
        ]
        
        for codename, name in permissions:
            Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={'name': name}
            )
