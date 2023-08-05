from . import db
# from FlaskTask import Base, session
from datetime import timedelta


class Counterparty(db.Model):
    __tablename__ = 'Counterparty'

    id = db.Column(db.Integer, primary_key=True)
    sysName = db.Column(db.String(250), nullable=False, unique=True)
    name = db.Column(db.String(250), nullable=False)
    setDate = db.Column(db.Integer())


class Company(db.Model):
    __tablename__ = 'Company'

    id = db.Column(db.Integer, primary_key=True)
    sysName = db.Column(db.String(250), nullable=False, unique=True)
    name = db.Column(db.String(250), nullable=False)
    setDate = db.Column(db.Integer())
