#!/usr/bin/env bash
# run.sh

set -o errexit

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn GenAIRevolution.wsgi:application --bind 0.0.0.0:$PORT