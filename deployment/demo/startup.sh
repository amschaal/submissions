#! /bin/sh
python /usr/src/app/manage.py runserver 0.0.0.0:8000
service nginx start