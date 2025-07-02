#!/bin/bash
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py load_data  # or however your script is named
gunicorn project.wsgi:application
