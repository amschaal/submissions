#! /bin/sh
service nginx start
cd /usr/src/app/
mkdir -p /data/media /data/static
python manage.py collectstatic --noinput 
python manage.py createcachetable
# gunicorn dnaorder.wsgi:application --bind 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000
