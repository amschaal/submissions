#! /bin/sh
service nginx start
cd /usr/src/app/
python manage.py collectstatic --noinput 
gunicorn dnaorder.wsgi:application --bind 0.0.0.0:8000

