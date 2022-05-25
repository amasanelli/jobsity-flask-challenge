# encoding: utf-8

import json


def test_invalid_token(client):
    """
    Invalid token
    """
    auth = '00.11.22'
    response = client.get('/api/v1/stock?q=aapl.us', headers={'Authorization': 'Bearer ' + auth})
    assert response.status_code == 400


def test_route_stock_unauthenticated(client):
    """
    Stock route unauthenticated
    """
    response = client.get('/api/v1/stock?q=aapl.us')
    assert response.status_code == 400


def test_route_stock_without_parameter(client, regular_user_token):
    """
    Stock route without parameter
    """
    response = client.get('/api/v1/stock', headers={'Authorization': 'Bearer ' + regular_user_token})
    assert response.status_code == 400


def test_route_stock_empty_parameter(client, regular_user_token):
    """
    Stock route with empty parameter
    """
    response = client.get('/api/v1/stock?q=', headers={'Authorization': 'Bearer ' + regular_user_token})
    assert response.status_code == 400


def test_route_stock_invalid_parameter(client, regular_user_token):
    """
    Stock route with invalid parameter
    """
    response = client.get('/api/v1/stock?q=19293847', headers={'Authorization': 'Bearer ' + regular_user_token})
    assert response.status_code == 400


def test_route_stock_valid_parameter_authenticated(client, regular_user_token):
    """
    Stock route with valid parameter and authenticated user
    """
    response = client.get('/api/v1/stock?q=aapl.us', headers={'Authorization': 'Bearer ' + regular_user_token})
    assert response.status_code == 200


def test_route_stock_response(client, regular_user_token):
    """
    Stock route response
    """
    response = client.get('/api/v1/stock?q=aapl.us', headers={'Authorization': 'Bearer ' + regular_user_token})
    json_data = json.loads(response.data.decode('utf8'))
    assert 'symbol' in json_data
    assert 'company_name' in json_data
    assert 'quote' in json_data


def test_route_user_history_unauthenticated(client):
    """
    History route with unauthenticated user
    """
    response = client.get('/api/v1/users/history')
    assert response.status_code == 400


def test_route_user_history_authenticated(client, regular_user_token):
    """
    History route with authenticated user
    """
    response = client.get('/api/v1/users/history', headers={'Authorization': 'Bearer ' + regular_user_token})
    assert response.status_code == 200


def test_route_user_history_response(client, regular_user_token):
    """
    History route response
    """
    response = client.get('/api/v1/users/history', headers={'Authorization': 'Bearer ' + regular_user_token})
    json_data = json.loads(response.data.decode('utf8'))
    assert 'symbol' in json_data[0]
    assert 'name' in json_data[0]
    assert 'date' in json_data[0]
    assert 'open' in json_data[0]
    assert 'low' in json_data[0]
    assert 'high' in json_data[0]
    assert 'close' in json_data[0]


def test_route_stats_unauthenticated(client, admin_user_token):
    """
    Stats route with unauthenticated user
    """
    response = client.get('/api/v1/stats')
    assert response.status_code == 400


def test_route_stats_authenticated(client, admin_user_token):
    """
    Stats route with authenticated user
    """
    response = client.get('/api/v1/stats', headers={'Authorization': 'Bearer ' + admin_user_token})
    assert response.status_code == 200


def test_route_stats_authenticated_unauthorized(client, regular_user_token):
    """
    Stats route authenticated but unauthorized user
    """
    response = client.get('/api/v1/stats', headers={'Authorization': 'Bearer ' + regular_user_token})
    assert response.status_code == 400


def test_route_stats_response(client, admin_user_token):
    """
    Stats route response
    """
    response = client.get('/api/v1/stats', headers={'Authorization': 'Bearer ' + admin_user_token})
    json_data = json.loads(response.data.decode('utf8'))
    assert 'stock' in json_data[0]
    assert 'times_requested' in json_data[0]


def test_route_login_valid_user(client):
    """
    Login route valid user
    """
    response = client.post('/api/v1/login', json={"username": "admin", "password": "admin"})
    assert response.status_code == 200


def test_route_login_invalid_user(client):
    """
    Login route invalid user
    """
    response = client.post('/api/v1/login', json={"username": "admin", "password": "test"})
    assert response.status_code == 400

def test_route_login_inactive_user(client):
    """
    Login route inactive user
    """
    response = client.post('/api/v1/login', json={"username": "inactive", "password": "inactive"})
    assert response.status_code == 400
