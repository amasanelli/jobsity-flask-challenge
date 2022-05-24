# encoding: utf-8

from flask import request
from flask_restful import Resource
from src.api.v_1_0.schemas import StockSchema
from src.auth import login_required
from src.models import StockQueryModel


class History(Resource):
    """
    Endpoint to see queries history
    """

    @login_required
    def get(self):
        """
        Returns queries made by the logged in user
        """

        stock_queries = StockQueryModel.query.filter_by(
            user_id=request.user.get('id')
        ).order_by(
            StockQueryModel.query_date.desc()
        ).all()

        schema = StockSchema(many=True)
        return schema.dump(stock_queries)
