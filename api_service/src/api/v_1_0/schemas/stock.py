# encoding: utf-8

from src.extensions import ma


class StockInfoSchema(ma.Schema):
    symbol = ma.String(dump_only=True)
    company_name = ma.String(dump_only=True)
    quote = ma.Float(dump_only=True)


class StockSchema(ma.Schema):
    symbol = ma.String(dump_only=True)
    name = ma.String(dump_only=True)
    query_date = ma.DateTime(dump_only=True, data_key='date')
    open = ma.Float(dump_only=True)
    high = ma.Float(dump_only=True)
    low = ma.Float(dump_only=True)
    close = ma.Float(dump_only=True)

class StockStatsSchema(ma.Schema):
    stock = ma.String(dump_only=True)
    times_requested = ma.Integer(dump_only=True)
