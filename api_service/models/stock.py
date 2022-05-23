from sqlalchemy import ForeignKey, func
from api_service.extensions import db

class Stock(db.Model):
    """ 
    Stock model 
    """

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    query_date = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, ForeignKey("user.id"))

    def __repr__(self):
        return "<Stock %s>" % self.symbol