# encoding: utf-8

from src.api.v_1_0.schemas import StockSchema
from datetime import datetime


def test_stock_schema():
    """
    Stock schema
    """
    result = StockSchema().dump(
        {
            "time": datetime.strptime("2022-05-24 22:00:06", "%Y-%m-%d %H:%M:%S").time(),
            "close": 140.36,
            "open": 140.805,
            "low": 137.33,
            "name": "APPLE",
            "date": datetime.strptime("2022-05-24 22:00:06", "%Y-%m-%d %H:%M:%S"),
            "high": 141.97,
            "symbol": "AAPL.US"
        }
    )
    assert {
        "time": "22:00:06",
        "close": 140.36,
        "open": 140.805,
        "low": 137.33,
        "name": "APPLE",
        "date": "2022-05-24",
        "high": 141.97,
        "symbol": "AAPL.US"
    } == result
