# encoding: utf-8

from flask import request
from flask_restful import Resource

from stock_service.api.v_1_0.schemas.stock import StockSchema
from stock_service.services import Stooq


class StockResource(Resource):
    """
    Endpoint that is in charge of aggregating the stock information from external sources and returning
    them to our main API service. Currently we only get the data from a single external source:
    the stooq API.
    """

    def get(self):
        stock_code = request.args.get('stockCode')

        if stock_code is None or stock_code == '':
            return "Missing stock code", 400

        try:
            stock_data_obj = Stooq.get_data(stock_code)
        except Exception as e:
            return e.args[0], 400

        schema = StockSchema()
        return schema.dump(stock_data_obj)
