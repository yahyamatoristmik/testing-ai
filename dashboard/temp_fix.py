# temp_fix.py
import django
from django.apps import apps
from django.db import models

# Non-aktifkan sementara post_migrate signal
from django.core.management.sql import emit_post_migrate_signal
from django.db.migrations.executor import MigrationExecutor
from django.db import connections

def safe_migrate():
    from django.core.management.commands import migrate
    
    # Override untuk skip contenttypes dan permissions sementara
    original_handle = migrate.Command.handle
    
    def safe_handle(self, *args, **options):
        # Skip post-migrate signals
        options['run_syncdb'] = False
        return original_handle(self, *args, **options)
    
    migrate.Command.handle = safe_handle

if __name__ == "__main__":
    safe_migrate()
