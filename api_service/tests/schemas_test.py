# encoding: utf-8

from src.api.v_1_0.schemas import StockSchema, StockInfoSchema, StockStatsSchema, UserSchema
from datetime import datetime


def test_user_schema():
    """
    User schema
    """
    result = UserSchema().dump(
        {
            "id": 1,
            "password": "admin",
            "email": "admin@admin.com",
            "username": "admin",
            "active": True,
            "role": "ADMIN"
        }
    )
    assert {
        "id": 1,
        "username": "admin",
        "role": "ADMIN"
    } == result


def test_stock_schema():
    """
    Stock schema
    """
    result = StockSchema().dump(
        {
            "symbol": "AAPL.US",
            "query_date": datetime.strptime("2022-05-23 15:03:56", "%Y-%m-%d %H:%M:%S"),
            "low": 137.65,
            "open": 137.79,
            "name": "APPLE",
            "close": 142.81,
            "high": 143.26
        }
    )
    assert {
        "symbol": "AAPL.US",
        "date": "2022-05-23T15:03:56",
        "low": 137.65,
        "open": 137.79,
        "name": "APPLE",
        "close": 142.81,
        "high": 143.26
    } == result


def test_stock_info_schema():
    """
    Stock info schema
    """
    result = StockInfoSchema().dump(
        {
            "company_name": "APPLE",
            "quote": 142.81,
            "symbol": "AAPL.US"
        }
    )
    assert {
        "company_name": "APPLE",
        "quote": 142.81,
        "symbol": "AAPL.US"
    } == result


def test_stock_stats_schema():
    """
    Stock stats schema
    """
    result = StockStatsSchema().dump(
        {
            "stock": "AAPL.US",
            "times_requested": 10
        }
    )
    assert {
        "stock": "AAPL.US",
        "times_requested": 10
    } == result
