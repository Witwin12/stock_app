#!/bin/sh
set -e

# 1. รัน Migrations 
echo "Running migrations..."
python manage.py migrate --noinput

# 2. รัน Collect Static
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 3. สร้าง Superuser 

echo "Creating superuser from .env variables (if not exists)..."

python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and email and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f'Superuser created: {username}')
    else:
        print(f'Superuser already exists: {username}')
else:
    print('DJANGO_SUPERUSER variables not set in .env. Skipping creation.')
EOF



echo "Starting Gunicorn..."
exec gunicorn stock_api.wsgi:application --bind 0.0.0.0:8000