#!/bin/sh
set -e


echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn stock_api.wsgi:application --bind 0.0.0.0:8000
