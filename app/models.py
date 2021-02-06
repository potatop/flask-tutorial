from datetime import datetime
from app import db

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    instock = db.Column(db.Boolean())
    price = db.Column(db.Numeric())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __repr__(self):
        return '<History {} {} {} {}>'.format(self.timestamp, self.name, self.instock, self.price)

