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
            identity = get_identity()
        except Exception as e:
            return e.args[0], 400

        if identity.get('role') == 'ADMIN':
            setattr(request, 'user', identity)
            return function(*args, **kwargs)

        return 'Unauthorized user', 400

    return wrapper


def login_required(function):
    """
    Decorator to check admin user
    """

    def wrapper(*args, **kwargs):
        try:
            identity = get_identity()
        except Exception as e:
            return e.args[0], 400
        
        setattr(request, 'user', identity)
        return function(*args, **kwargs)

    return wrapper

def get_identity():
    token = request.headers.get('Authorization')

    if token is None:
        raise Exception('Missing authorization header')

    token = token.replace('Bearer ', '')

    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], ["HS256"])
    except:
        raise Exception('Invalid token')

    identity = payload.get('identity')

    if identity is None:
        raise Exception('Invalid token')

    return identity
