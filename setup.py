import os
import sys
import django
from django.core.management import execute_from_command_line
from django.conf import settings

def setup_project():
    """
    Complete setup for Django App Search Application
    """
    print("🚀 Setting up Django App Search Application...")
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    django.setup()
    
    # Check if database file exists
    db_path = settings.DATABASES['default']['NAME']
    print(f"📊 Database path: {db_path}")
    
    if not os.path.exists(db_path):
        print("📁 Creating SQLite database file...")
        # The database file will be created automatically when we run migrate
    else:
        print("✅ Database file already exists")
    
    print("📝 Creating migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✅ Migrations created successfully")
    except Exception as e:
        print(f"⚠️ Error creating migrations: {e}")
        return False
    
    print("🗄️ Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️ Error running migrations: {e}")
        return False
    
    print("🔧 Creating superuser (optional)...")
    try:
        # You can uncomment this if you want to create a superuser automatically
        # execute_from_command_line(['manage.py', 'createsuperuser', '--noinput', 
        #                           '--username=admin', '--email=admin@example.com'])
        print("💡 Run 'python manage.py createsuperuser' manually to create an admin user")
    except Exception as e:
        print(f"⚠️ Note: {e}")
    
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run 'python manage.py runserver' to start the development server")
    print("2. Visit http://127.0.0.1:8000 to access your application")
    print("3. Create a superuser with 'python manage.py createsuperuser' if needed")
    
    return True

if __name__ == '__main__':
    success = setup_project()