# encoding: utf-8

from stock_service.extensions import ma


class StockSchema(ma.Schema):

    symbol = ma.String(dump_only=True)
    name = ma.String(dump_only=True)
    date = ma.Date(dump_only=True)
    time = ma.Time(dump_only=True)
    open = ma.Float(dump_only=True)
    high = ma.Float(dump_only=True)
    low = ma.Float(dump_only=True)
    close = ma.Float(dump_only=True)
