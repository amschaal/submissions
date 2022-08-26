#! /bin/sh
service nginx start
python /usr/src/app/manage.py runserver 0.0.0.0:8000
