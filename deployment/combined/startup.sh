#! /bin/sh
service nginx start
cd /usr/src/app/
echo "Collect static"
python manage.py collectstatic
gunicorn dnaorder.wsgi:application --bind 0.0.0.0:8000

