from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from django.urls import reverse
from .models import DataLeakConfig, DataLeakScan, UserDataLeakPermission

@admin.register(DataLeakConfig)
class DataLeakConfigAdmin(admin.ModelAdmin):
    list_display = ['is_active', 'api_url', 'created_by', 'created_at']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DataLeakScan)
class DataLeakScanAdmin(admin.ModelAdmin):
    list_display = ['target', 'scan_type', 'status', 'requested_by', 'created_at']
    list_filter = ['status', 'scan_type']
    search_fields = ['target']

@admin.register(UserDataLeakPermission)
class UserDataLeakPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'can_access_data_leak', 'granted_at', 'granted_by']
    list_filter = ['can_access_data_leak']
