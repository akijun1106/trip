#!/bin/bash
set -eu

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_admin

echo "Build completed successfully"
