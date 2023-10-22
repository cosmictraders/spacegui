from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    token = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)


class Automation(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    icon = db.Column(db.String, nullable=True)
    text = db.Column(db.String, nullable=False)
