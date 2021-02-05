import celery
from flask import render_template
from app.models import History
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/log')
def log():
    his = History.query.order_by(History.timestamp.desc()).limit(15).all()
    return render_template('log.html', title='Log', posts=his)

