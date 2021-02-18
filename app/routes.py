from flask import render_template
from app.models import Price, Product
from sqlalchemy.sql.expression import func
from app import app, db

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/log')
def log():
    q = db.session.query(Price, func.rank().over(partition_by=Price.product_id, order_by=Price.timestamp.desc()).label('rank')).subquery()
    prices = db.session.query(Price).select_entity_from(q).filter(q.c.rank == 1, Price.instock == True).all()
    return render_template('log.html', title='Log', items=prices)

