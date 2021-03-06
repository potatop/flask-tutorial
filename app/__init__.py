import celery
from flask import Flask
from config import Config
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

celery = Celery(app.name)
celery.conf.update(
    broker_url = app.config["CELERY_BROKER_URL"],
    result_backend = app.config["CELERY_BROKER_URL"],
    # beat_schedule = {
    #     "microcenter-task": {
    #         "task": "app.tasks.microcenter",
    #         "schedule": app.config["SCHEDULE"]
    #     }
    # }
)

from app import routes, models, tasks