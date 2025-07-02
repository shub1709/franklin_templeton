import os
import django
from django.core.management import call_command
from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

print("👉 Running migrate...")
call_command("migrate")

print("👉 Collecting static files...")
call_command("collectstatic", interactive=False)

print("👉 Creating default superuser...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
    print("✅ Superuser created: admin / adminpassword")

print("👉 Loading data...")
call_command("load_data")
