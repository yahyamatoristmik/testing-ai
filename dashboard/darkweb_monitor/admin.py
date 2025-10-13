from django.contrib import admin
from .models import DarkWebConfig, DarkWebScan, DarkWebFinding, UserDarkWebPermission

@admin.register(DarkWebConfig)
class DarkWebConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active', 'created_by', 'created_at']  # Tambahkan 'id'
    list_editable = ['is_active']  # Hanya 'is_active' yang editable
    list_display_links = ['id']  # Tambahkan ini
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DarkWebScan)
class DarkWebScanAdmin(admin.ModelAdmin):
    list_display = ['target', 'scan_type', 'status', 'risk_score', 'requested_by', 'created_at']
    list_filter = ['status', 'scan_type', 'created_at']
    search_fields = ['target']

@admin.register(DarkWebFinding)
class DarkWebFindingAdmin(admin.ModelAdmin):
    list_display = ['scan', 'source', 'finding_type', 'risk_level', 'data_points', 'created_at']
    list_filter = ['source', 'risk_level', 'created_at']

@admin.register(UserDarkWebPermission)
class UserDarkWebPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'can_access_darkweb', 'granted_at', 'granted_by']
    list_filter = ['can_access_darkweb']
