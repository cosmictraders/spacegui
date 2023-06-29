from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    token = db.Column(db.String, nullable=False)


class Automation(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    text = db.Column(db.String, nullable=False)
