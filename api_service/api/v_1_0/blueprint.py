# encoding: utf-8

from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from .resourses import StockQuery, History, Stats


api_v1_0_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_v1_0_bp)


api.add_resource(StockQuery, "/stock", endpoint="stock")
api.add_resource(History, "/users/history", endpoint="users-history")
api.add_resource(Stats, "/stats", endpoint="stats")


@api_v1_0_bp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
