#!/bin/bash
set -e

if [[ $ENVIRONMENT == "local" ]]; then
    bash docker/init.sh
    exec python manage.py runserver 0.0.0.0:${APP_PORT} --traceback
else
    GUNICORN_ARGS=(
        "--bind=0.0.0.0:8000"
        "--timeout=${GUNICORN_TIMEOUT:-180}"
        "--workers=${GUNICORN_WORKERS:-2}"
    )
    DJANGO_SETTINGS_MODULE=pilitlot.settings GUNICORN_CMD_ARGS="${GUNICORN_ARGS[*]}" exec gunicorn pilitlot.wsgi
fi
