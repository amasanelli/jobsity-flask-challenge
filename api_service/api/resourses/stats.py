from flask import request
from flask_restful import Resource
from api_service.api.schemas import StockInfoSchema
from api_service.extensions import db


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """

    def get(self):
        # TODO: Implement this method.
        pass
