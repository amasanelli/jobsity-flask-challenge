from sqlalchemy import ForeignKey
from api_service.extensions import db
from datetime import datetime

class StockQueryModel(db.Model):
    """ 
    Stock model 
    """

    __tablename__ = 'stock_query'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time =  db.Column(db.Time, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    query_date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<Stock %s>" % self.symbol