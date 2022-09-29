#! /bin/sh
service nginx start
pg_restore --clean --no-owner -d postgres /usr/src/app/deployment/demo/demo.coreomics.com.dump --user=postgres --host=db --port=5432
python /usr/src/app/manage.py runserver 0.0.0.0:8000

