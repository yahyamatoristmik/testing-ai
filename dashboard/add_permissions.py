from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

# Cari user admin
admin_user = User.objects.get(username='admin')

# Berikan semua permissions untuk sast_report
content_types = ContentType.objects.filter(app_label='sast_report')
permissions = Permission.objects.filter(content_type__in=content_types)
admin_user.user_permissions.add(*permissions)
admin_user.save()

print("Permissions berhasil diberikan untuk user:", admin_user.username)
