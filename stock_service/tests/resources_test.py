# encoding: utf-8

import pytest
import requests
import json


@pytest.mark.dependency()
def test_stooq():
    """
    Stooq.com online
    """
    response = requests.get('https://stooq.com')
    assert response.status_code == 200


@pytest.mark.dependency(depends=["test_stooq"])
def test_route_stock_without_parameter(client):
    """
    Stock route without parameter
    """
    response = client.get('/api/v1/stock')
    assert response.status_code == 400


@pytest.mark.dependency(depends=["test_stooq"])
def test_route_stock_empty_parameter(client):
    """
    Stock route with empty parameter
    """
    response = client.get('/api/v1/stock?stockCode=')
    assert response.status_code == 400


@pytest.mark.dependency(depends=["test_stooq"])
def test_route_stock_invalid_parameter(client):
    """
    Stock route with invalid parameter
    """
    response = client.get('/api/v1/stock?stockCode=test')
    assert response.status_code == 400


@pytest.mark.dependency(depends=["test_stooq"])
def test_route_stock_valid_parameter(client):
    """
    Stock route with invalid parameter
    """
    response = client.get('/api/v1/stock?stockCode=aapl.us')
    assert response.status_code == 200


@pytest.mark.dependency(depends=["test_stooq"])
def test_route_stock_response(client):
    """
    Stock route response
    """
    response = client.get('/api/v1/stock?stockCode=aapl.us')
    json_data = json.loads(response.data.decode('utf-8'))
    assert 'time' in json_data
    assert 'close' in json_data
    assert 'open' in json_data
    assert 'low' in json_data
    assert 'name' in json_data
    assert 'date' in json_data
    assert 'high' in json_data
    assert 'symbol' in json_data
