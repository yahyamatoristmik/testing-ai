# management/commands/set_scan_owners.py
from django.core.management.base import BaseCommand
from dast_reports.models import DASTScan
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Set default owner for existing DAST scans'

    def handle(self, *args, **options):
        # Set owner untuk scan yang sudah ada
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            scans_without_owner = DASTScan.objects.filter(owner__isnull=True)
            count = scans_without_owner.count()
            
            if count > 0:
                scans_without_owner.update(owner=superuser)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully set owner for {count} scans to {superuser.username}"
                    )
                )
            else:
                self.stdout.write("All scans already have owners")
        else:
            self.stdout.write(
                self.style.ERROR("No superuser found to set as owner")
            )
