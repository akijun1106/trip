web: gunicorn config.wsgi --workers 2 --worker-class sync --timeout 60 --access-logfile - --bind 0.0.0.0:${PORT:-8000}
release: python manage.py migrate && python manage.py collectstatic --noinput
