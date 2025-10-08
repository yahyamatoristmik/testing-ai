# force_migrate.py
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connections
from django.db.migrations.executor import MigrationExecutor

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

def force_migrate():
    # Disable ALL post_migrate signals
    from django.db.models.signals import post_migrate
    
    def disable_signal(sender, **kwargs):
        pass
    
    # Disable specific signals
    post_migrate.disconnect(dispatch_uid="django.contrib.auth.management.create_permissions")
    post_migrate.disconnect(dispatch_uid="django.contrib.contenttypes.management.create_contenttypes")
    
    # Run migrate without signals
    from django.core.management.commands.migrate import Command as MigrateCommand
    from django.db import connection
    
    print("Running migrations without post-migrate signals...")
    
    # Get current migration state
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    
    # Run migrations
    plan = executor.migration_plan(targets)
    for migration, _ in plan:
        print(f"Applying {migration}")
        executor.apply_migration(migration, fake=False)
    
    print("Migrations completed successfully!")

if __name__ == '__main__':
    force_migrate()
