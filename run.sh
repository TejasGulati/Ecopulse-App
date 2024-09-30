#!/usr/bin/env bash
# run.sh

set -o errexit

cd backend
python manage.py migrate
gunicorn GenAIRevolution.wsgi:application --bind 0.0.0.0:$PORT