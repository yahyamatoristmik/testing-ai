from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect

def sast_permission_required(permission):
    """
    Decorator untuk check permission SAST yang strict
    """
    def check_permission(user):
        # Superuser selalu bisa akses
        if user.is_superuser:
            return True
        # Check specific permission
        return user.has_perm(permission)
    
    return user_passes_test(
        check_permission, 
        login_url='/',
        redirect_field_name=None
    )

def sast_access_required():
    """
    Decorator untuk check minimal satu SAST permission
    """
    def check_user(user):
        # Superuser selalu bisa akses
        if user.is_superuser:
            return True
            
        # Check minimal satu SAST permission
        sast_permissions = [
            'sast_report.can_view_sast',
            'sast_report.can_manage_scm', 
            'sast_report.can_run_scan',
            'sast_report.can_view_reports'
        ]
        
        return any(user.has_perm(perm) for perm in sast_permissions)
    
    return user_passes_test(
        check_user, 
        login_url='/',
        redirect_field_name=None
    )
