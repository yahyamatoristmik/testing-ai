from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from sast_report.models import SCMProfile

class Command(BaseCommand):
    help = 'Setup SAST permissions and groups'
    
    def handle(self, *args, **options):
        # Buat permissions
        content_type = ContentType.objects.get_for_model(SCMProfile)
        
        permissions_data = [
            ('can_view_sast', 'Can view SAST dashboard'),
            ('can_manage_scm', 'Can manage SCM profiles'),
            ('can_run_scan', 'Can run security scans'),
            ('can_view_reports', 'Can view scan reports'),
        ]
        
        permissions = []
        for codename, name in permissions_data:
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={'name': name}
            )
            permissions.append(perm)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created permission: {name}'))
        
        # Buat groups
        groups_data = {
            'sast_viewer': ['can_view_sast', 'can_view_reports'],
            'sast_operator': ['can_view_sast', 'can_run_scan', 'can_view_reports'],
            'sast_admin': ['can_view_sast', 'can_manage_scm', 'can_run_scan', 'can_view_reports'],
        }
        
        for group_name, permission_codenames in groups_data.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            # Clear existing permissions
            group.permissions.clear()
            
            # Add new permissions
            for codename in permission_codenames:
                perm = Permission.objects.get(codename=codename, content_type=content_type)
                group.permissions.add(perm)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated group: {group_name}'))
        
        self.stdout.write(self.style.SUCCESS('✅ SAST permissions setup completed!'))
