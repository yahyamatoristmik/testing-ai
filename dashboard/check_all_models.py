import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import Repository, UserSCMProfile
from django.contrib.auth.models import User

def inspect_all_models():
    print("🔍 INSPECTING ALL MODEL STRUCTURES")
    print("=" * 60)
    
    # Check Repository model
    print("\n📋 REPOSITORY MODEL FIELDS:")
    repo_fields = Repository._meta.get_fields()
    for field in repo_fields:
        field_info = f"  - {field.name} ({field.get_internal_type()})"
        if field.is_relation:
            field_info += f" -> {field.related_model.__name__}"
        print(field_info)
    
    # Check UserSCMProfile model  
    print("\n📋 USER SCM PROFILE MODEL FIELDS:")
    scm_fields = UserSCMProfile._meta.get_fields()
    for field in scm_fields:
        field_info = f"  - {field.name} ({field.get_internal_type()})"
        if field.is_relation:
            field_info += f" -> {field.related_model.__name__}"
        print(field_info)
    
    # Check existing data
    print(f"\n📊 EXISTING DATA:")
    print(f"  - Users: {User.objects.count()}")
    print(f"  - SCM Profiles: {UserSCMProfile.objects.count()}")
    print(f"  - Repositories: {Repository.objects.count()}")
    
    # Show sample SCM profiles
    if UserSCMProfile.objects.exists():
        print(f"\n📄 SAMPLE SCM PROFILES:")
        for profile in UserSCMProfile.objects.all()[:3]:
            print(f"  - {profile.user.username}: {profile.scm_type} ({profile.username})")

if __name__ == '__main__':
    inspect_all_models()
