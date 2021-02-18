from datetime import datetime
from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    prices = db.relationship('Price', backref='product', lazy='dynamic')

    def __repr__(self):
        return '<Product {}>'.format(self.name)
        
class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instock = db.Column(db.Boolean())
    price = db.Column(db.Numeric())
    premium = db.Column(db.Numeric(), default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    
    def __repr__(self):
        return '<Price {} {} {}>'.format(self.instock, self.price, self.timestamp)

