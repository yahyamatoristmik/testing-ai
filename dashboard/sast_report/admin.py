from django.contrib import admin
from .models import SCMProfile, Repository, ScanJob, Finding

@admin.register(SCMProfile)
class SCMProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'scm_type', 'username', 'is_active', 'created_at']
    list_filter = ['scm_type', 'is_active']
    search_fields = ['user__username', 'username']
    readonly_fields = ['created_at']

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'scm_profile', 'default_branch', 'is_active', 'created_at']
    list_filter = ['is_active', 'scm_profile__scm_type']
    search_fields = ['name', 'url']
    readonly_fields = ['created_at']

@admin.register(ScanJob)
class ScanJobAdmin(admin.ModelAdmin):
    list_display = ['repository', 'status', 'branch', 'total_findings', 'created_at', 'duration_display']
    list_filter = ['status', 'created_at']
    search_fields = ['repository__name']
    readonly_fields = ['created_at', 'started_at', 'completed_at']
    
    def duration_display(self, obj):
        return obj.get_duration_display()
    duration_display.short_description = 'Duration'

@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ['rule_id', 'severity', 'file_path', 'line_number', 'scan_job']
    list_filter = ['severity', 'created_at']
    search_fields = ['rule_id', 'file_path', 'message']
    readonly_fields = ['created_at']
