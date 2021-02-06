web: flask db upgrade; gunicorn microblog:app --log-file -
worker: celery -A app.celery worker -B -l INFO 