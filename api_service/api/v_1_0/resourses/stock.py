from flask import request
from flask_restful import Resource
from api_service.api.v_1_0.schemas import StockInfoSchema
from api_service.extensions import db
from api_service.services import StockService


class StockQuery(Resource):
    """
    Endpoint to allow users to query stocks
    """

    def get(self):
        
        stock_code = request.args.get('q')

        if stock_code is None or stock_code == '':
            return 'Missing stock code', 400

        try:
            stock_data = StockService.get_data(stock_code)
        except Exception as e:
            return e.args[0], 400

        schema = StockInfoSchema()
        return schema.dump({
            'symbol': stock_data.get('symbol'),
            'company_name': stock_data.get('name'),
            'quote': stock_data.get('close')
        })
