from flask import request
from flask_restful import Resource
from api_service.api.v_1_0.schemas import StockInfoSchema
from api_service.extensions import db
from api_service.auth import admin_required


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """

    @admin_required
    def get(self):
        # TODO: Implement this method.
        return request.user
