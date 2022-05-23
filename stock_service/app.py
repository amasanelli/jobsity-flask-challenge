from flask import Flask
from .api import blueprint
from stock_service import rpc_server
from .extensions import ma

def create_app(testing=False):
    app = Flask("stock_service")
    app.config.from_object("stock_service.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)

    return app

def configure_extensions(app):
    ma.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blueprint)
