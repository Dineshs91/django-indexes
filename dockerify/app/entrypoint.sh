#! /bin/bash

set -e

until export PGPASSWORD=$POSTGRES_PASSWORD; psql -h $POSTGRES_HOST -U $POSTGRES_USER --dbname $POSTGRES_DB -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

python manage.py migrate


gunicorn djangothon.wsgi --log-level="$log_level" -k eventlet -w 1 -b 0.0.0.0:8091 --reload
