# encoding: utf-8

from flask import jsonify, request
from flask_restful import Resource
from src.auth import create_access_token
from src.api.v_1_0.schemas import UserSchema
from src.extensions import bcrypt
from src.models import UserModel


class Login(Resource):
    """
    Endpoint for user login
    """

    def post(self):
        """
        Uses the username and password from the JSON body to generate and return a JWT token
        """

        req_data = request.get_json()

        username = req_data.get('username')
        password = req_data.get('password')

        if username is None or password is None:
            return "Missing login credentials", 400

        user: UserModel = UserModel.query.filter_by(username=username).first()
        if user is None:
            return "User not found", 400

        if not bcrypt.check_password_hash(user.password, password):
            return "Unauthorized user", 400

        schema = UserSchema()
        token_data = schema.dump(user)
        access_token = create_access_token(token_data)

        return jsonify({'token': access_token})
