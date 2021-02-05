web: flask db upgrade; flask translate compile; gunicorn microblog:app
worker: celery -A app.celery worker -B -l INFO 