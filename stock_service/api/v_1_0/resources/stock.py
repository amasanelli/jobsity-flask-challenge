# encoding: utf-8

from flask import request
from flask_restful import Resource

from stock_service.api.v_1_0.schemas.stock import StockSchema
from stock_service.services.stooq import Stooq


class StockResource(Resource):
    """
    Endpoint that is in charge of aggregating the stock information from external sources and returning
    them to our main API service. Currently we only get the data from a single external source:
    the stooq API.
    """

    def get(self):
        # TODO: Implement the call to the stooq service here. The stock code to query the API
        # should come in a query parameter.

        stock_code = request.args.get('stockCode')

        if stock_code is None or stock_code == '':
            return "Missing stock code", 400

        stock_data_obj = Stooq.get_data(stock_code)

        if stock_data_obj is None:
            return "No data", 400

        schema = StockSchema()
        return schema.dump(stock_data_obj)
