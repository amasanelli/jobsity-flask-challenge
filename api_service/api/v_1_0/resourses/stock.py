from flask import request
from flask_restful import Resource
from api_service.api.v_1_0.schemas import StockInfoSchema
from api_service.extensions import db


class StockQuery(Resource):
    """
    Endpoint to allow users to query stocks
    """

    def get(self):
        # TODO: Call the stock service, save the response, and return the response to the user in
        # the format dictated by the StockInfoSchema.
        data_from_service = None
        schema = StockInfoSchema()
        return schema.dump(data_from_service)
