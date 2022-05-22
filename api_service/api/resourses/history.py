from flask import request
from flask_restful import Resource
from api_service.api.schemas import StockInfoSchema
from api_service.extensions import db


class History(Resource):
    """
    Returns queries made by current user.
    """

    def get(self):
        # TODO: Implement this method.
        pass
