#! /bin/sh
service nginx start
cd /usr/src/app/
gunicorn dnaorder.wsgi:application --bind 0.0.0.0:8000

