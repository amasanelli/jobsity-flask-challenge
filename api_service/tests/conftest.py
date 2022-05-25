# encoding: utf-8

from datetime import datetime, timedelta
import jwt
import pytest

from dotenv import load_dotenv

from src.api.v_1_0.schemas import UserSchema
from src.models import UserModel
from src.app import create_app
from src.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture(scope="session")
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

    exists = UserModel.query.filter_by(username=user.username).first()
    if not exists:
        db.session.add(user)
        db.session.commit()

    return user


@pytest.fixture
def regular_user(db):
    user = UserModel(
        username='johndoe',
        email='johndoe@admin.com',
        password='john',
        role='USER'
    )

    exists = UserModel.query.filter_by(username=user.username).first()
    if not exists:
        db.session.add(user)
        db.session.commit()

    return user

@pytest.fixture
def inactive_user(db):
    user = UserModel(
        username='inactive',
        email='inactive@admin.com',
        password='inactive',
        role='USER',
        active=False
    )

    exists = UserModel.query.filter_by(username=user.username).first()
    if not exists:
        db.session.add(user)
        db.session.commit()

    return user

@pytest.fixture
def client(app):
    context = app.app_context()
    context.push()
    with context:
        with app.test_client() as client:
            yield client
    context.pop()


@pytest.fixture
def admin_user_token(app, admin_user):
    return jwt.encode(
        {
            'identity': UserSchema().dump(admin_user),
            'exp': datetime.utcnow() + timedelta(minutes=60)
        },
        app.config['SECRET_KEY'],
        'HS256'
    )


@pytest.fixture
def regular_user_token(app, regular_user):
    return jwt.encode(
        {
            'identity': UserSchema().dump(regular_user),
            'exp': datetime.utcnow() + timedelta(minutes=60)
        },
        app.config['SECRET_KEY'],
        'HS256'
    )
