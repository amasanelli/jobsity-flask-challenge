from flask import request
from flask_restful import Resource
from sqlalchemy import func
from api_service.api.v_1_0.schemas import StockStatsSchema
from api_service.auth import admin_required
from api_service.extensions import db
from api_service.models import StockQueryModel


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """

    @admin_required
    def get(self):
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
