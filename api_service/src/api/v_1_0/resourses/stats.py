# encoding: utf-8

from flask import request
from flask_restful import Resource
from sqlalchemy import func
from src.api.v_1_0.schemas import StockStatsSchema
from src.auth import admin_required
from src.extensions import db
from src.models import StockQueryModel


class Stats(Resource):
    """
    Endpoint to see query stats
    Only ADMIN users allowed
    """

    @admin_required
    def get(self):
        """
        Returns the top 5 symbol 
        """

        stock_stats = db.session.query(
            StockQueryModel.symbol,
            func.count(StockQueryModel.id)
        ).group_by(
            StockQueryModel.symbol
        ).order_by(
            func.count(StockQueryModel.id).desc()
        ).limit(5).all()

        schema = StockStatsSchema(many=True)
        return schema.dump([{'stock': item[0], 'times_requested': item[1]} for item in stock_stats])
