# encoding: utf-8

from datetime import datetime
from random import randrange
from src.models import UserModel, StockQueryModel


def test_user_insert(db):
    """
    User insert
    """
    test_user = UserModel(
        username='test',
        email='test@test.com',
        password='test',
        role='USER'
    )

    db.session.add(test_user)
    db.session.commit()

    response = UserModel.query.filter_by(username=test_user.username).first()
    assert test_user.username == response.username
    assert test_user.email == response.email
    assert test_user.password == response.password
    assert test_user.role == response.role
    assert test_user.active == response.active


def test_stock_insert(db):
    """
    Stock insert
    """
    now = datetime.now()
    test_stock = StockQueryModel(
        symbol="AAPL.US",
        name="APPLE",
        date=now,
        time=now.time(),
        open=137.79,
        low=137.65,
        high=143.26,
        close=142.81,
        user_id=1,
        query_date=now
    )

    db.session.add(test_stock)
    db.session.commit()

    response = StockQueryModel.query.filter_by(symbol="AAPL.US").first()
    assert test_stock.symbol == response.symbol
    assert test_stock.name == response.name
    assert test_stock.open == response.open
    assert test_stock.low == response.low
    assert test_stock.high == response.high
    assert test_stock.close == response.close
    assert test_stock.date == response.date
    assert test_stock.user_id == response.user_id
    assert test_stock.query_date == response.query_date
