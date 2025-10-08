from django.contrib import admin
from .models import UserSCMProfile, Repository, ScanJob, VulnerabilityReport

@admin.register(UserSCMProfile)
class UserSCMProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'scm_type', 'created_at']

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'scm_profile', 'private']

@admin.register(ScanJob)
class ScanJobAdmin(admin.ModelAdmin):
    list_display = ['repository', 'user', 'status', 'triggered_at', 'findings_count']
    list_filter = ['status', 'triggered_at']

@admin.register(VulnerabilityReport)
class VulnerabilityReportAdmin(admin.ModelAdmin):
    list_display = ['rule_id', 'severity', 'file_path', 'scan_job']
    list_filter = ['severity']
