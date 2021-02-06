import celery
from flask import render_template
from app.models import History
from app import app
import requests

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/log')
def log():
    his = History.query.order_by(History.timestamp.desc()).limit(15).all()
    return render_template('log.html', title='Log', posts=his)

@app.route('/test', methods=['POST'])
def test_message():
    r = requests.post(app.config['TILL_URL'], json={
        "phone": ["16157152079"],
        "text" : "test message!"
    })
    return r