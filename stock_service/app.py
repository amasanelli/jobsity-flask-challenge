from flask import Flask
from stock_service.api import blueprint
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


if __name__ == '__main__':
    app = create_app(False)
    app.run(host='0.0.0.0', port=5001)
