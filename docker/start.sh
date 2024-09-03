#!/bin/bash
set -e

bash docker/init.sh

if [[ $ENVIRONMENT == "local" ]]; then
    exec python ./src/manage.py runserver 0.0.0.0:${APP_PORT} --traceback
else
    GUNICORN_ARGS=(
        "--bind=0.0.0.0:8000"
        "--timeout=${GUNICORN_TIMEOUT:-180}"
        "--workers=${GUNICORN_WORKERS:-2}"
        "--reload"
    )
    DJANGO_SETTINGS_MODULE=apexive.settings GUNICORN_CMD_ARGS="${GUNICORN_ARGS[*]}" exec gunicorn apexive.wsgi
fi
