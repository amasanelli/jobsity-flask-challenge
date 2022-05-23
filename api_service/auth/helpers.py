# encoding: utf-8

import jwt
from flask import current_app, request
from datetime import datetime, timedelta


def create_access_token(identity):
    return jwt.encode(
        {
            'identity': identity,
            'exp': datetime.utcnow() + timedelta(minutes=60)
        },
        current_app.config['SECRET_KEY'],
        "HS256")


def admin_required(function):
    """
    Decorator to check admin user
    """

    def wrapper(*args, **kwargs):
        try:
            payload = get_payload()
        except Exception as e:
            return e.args[0], 400

        if payload['identity']['role'] == 'ADMIN':
            setattr(request, 'user', payload['identity'])
            return function(*args, **kwargs)

        return 'Unauthorized user', 400

    return wrapper


def login_required(function):
    """
    Decorator to check admin user
    """

    def wrapper(*args, **kwargs):
        try:
            payload = get_payload()
        except Exception as e:
            return e.args[0], 400
        
        setattr(request, 'user', payload['identity'])
        return function(*args, **kwargs)

    return wrapper

def get_payload():
    token = request.headers.get('Authorization').replace('Bearer ', '')

    if token is None:
        raise Exception('Missing authorization header')

    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], ["HS256"])
    except:
        raise Exception('Invalid token')

    return payload
