from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from api_service.api.v_1_0.schemas import UserSchema
from api_service.extensions import db, bcrypt
from api_service.models import User


class Login(Resource):
    """
    User login
    """

    def post(self):
        req_data = request.get_json()

        username = req_data.get('username')
        password = req_data.get('password')

        if username is None or password is None:
            return "Missing login credentials", 400

        user: User = User.query.filter_by(username=username).first()
        if user is None:
            return "User not found", 400

        if not bcrypt.check_password_hash(user.password, password):
            return "Unauthorized user", 400


        schema = UserSchema()
        token_data = schema.dump(user)
        access_token = create_access_token(identity=token_data)

        return jsonify({'token': access_token})
