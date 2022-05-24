# encoding: utf-8

from src.extensions import ma


class UserSchema(ma.Schema):
    """
    User schema to use in JWT payload
    """
    
    id = ma.Integer(dump_only=True)
    username = ma.String(dump_only=True)
    role = ma.String(dump_only=True)