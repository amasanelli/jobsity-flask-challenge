# encoding: utf-8

from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from .resources import StockResource


api_v1_0_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_v1_0_bp)

api.add_resource(StockResource, "/stock", endpoint="stock")


@api_v1_0_bp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
