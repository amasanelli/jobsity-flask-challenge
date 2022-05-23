# encoding: utf-8

from api_service.extensions import ma


class UserSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    username = ma.String(dump_only=True)
    role = ma.String(dump_only=True)