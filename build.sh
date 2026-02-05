#!/bin/bash
set -eu

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

echo "Build completed successfully"
