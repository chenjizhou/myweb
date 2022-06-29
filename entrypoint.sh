#!/usr/bin/env bash
# Wait until MySQL is ready
while ! nc -z myweb.mysql 3306; do
    echo "Waiting for MySQL to be up..."
    sleep 1
done
flask db upgrade
python manage.py
