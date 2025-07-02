import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.core.management import call_command

# Run necessary commands
call_command("migrate")
call_command("createsuperuser", interactive=True)
call_command("collectstatic", interactive=False)
call_command("load_data")
