# encoding: utf-8

from datetime import datetime
import os
from flask import request
from flask_restful import Resource
from src.api.v_1_0.schemas import StockInfoSchema
from src.auth import login_required
from src.extensions import db
from src.models import StockQueryModel
from src.services import StockRPCService, StockHTTPService


class StockQuery(Resource):
    """
    Endpoint to query stocks
    """

    @login_required
    def get(self):
        """
        Returns stock data from stock service
        """

        stock_code = request.args.get('q')

        if stock_code is None or stock_code == '':
            return 'Missing stock code', 400

        try:
            if os.getenv('RPC') == 'enabled':
                stock_data = StockRPCService().get_data(stock_code)
            else:
                stock_data = StockHTTPService.get_data(stock_code)
        except Exception as e:
            return e.args[0], 400

        # save the stock data in db
        stock_query = StockQueryModel(
            symbol=stock_data.get('symbol'),
            name=stock_data.get('name'),
            date=datetime.strptime(stock_data.get('date'), '%Y-%m-%d'),
            time=datetime.strptime(stock_data.get('time'), '%H:%M:%S').time(),
            open=stock_data.get('open'),
            high=stock_data.get('high'),
            low=stock_data.get('low'),
            close=stock_data.get('close'),
            user_id=request.user.get('id'),
            query_date=datetime.now()
        )
        db.session.add(stock_query)
        db.session.commit()

        # return a simplified version of data
        schema = StockInfoSchema()
        return schema.dump({
            'symbol': stock_data.get('symbol'),
            'company_name': stock_data.get('name'),
            'quote': stock_data.get('close')
        })
