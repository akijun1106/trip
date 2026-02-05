web: gunicorn config.wsgi --workers 2 --worker-class sync --timeout 60 --access-logfile -
release: python manage.py migrate && python manage.py collectstatic --noinput
