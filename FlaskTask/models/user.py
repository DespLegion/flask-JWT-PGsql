from . import db
# from FlaskTask import Base
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt


class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def auth(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('Неверный пароль')
        return user

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # @classmethod
    # def sec_user_status(cls, sec_level):
