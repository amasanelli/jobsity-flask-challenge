# encoding: utf-8

import pytest

from dotenv import load_dotenv

from src.app import create_app


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def client(app):
    context = app.app_context()
    context.push()
    with context:
        with app.test_client() as client:
            yield client
    context.pop()
