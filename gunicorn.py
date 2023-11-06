from website.app import create_app
from website.config import BaseConfig


def app(db, secret_key):
    BaseConfig.SECRET_KEY = secret_key
    BaseConfig.SQLALCHEMY_DATABASE_URI = db
    return create_app()
