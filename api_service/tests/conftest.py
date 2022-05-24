# encoding: utf-8

import pytest
from dotenv import load_dotenv

from src.models import UserModel
from src.app import create_app
from src.extensions import db as _db
from pytest_factoryboy import register
from .factories import UserFactory


register(UserFactory)


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = UserModel(
        username='admin',
        email='admin@admin.com',
        password='admin',
        role='ADMIN'
    )

    db.session.add(user)
    db.session.commit()

    return user
