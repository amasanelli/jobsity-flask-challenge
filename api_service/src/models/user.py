# encoding: utf-8

from sqlalchemy.ext.hybrid import hybrid_property
from src.extensions import db, bcrypt


class UserModel(db.Model):
    """
    User model
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = bcrypt.generate_password_hash(value).decode('utf8')

    def __repr__(self):
        return "<User %s>" % self.username
