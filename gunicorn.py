from website.app import create_app
from website.config import BaseConfig
import os


def app():
    BaseConfig.SECRET_KEY = os.environ.get("SECRET_KEY")
    if os.environ.get("DATABASE_URL") is not None:
        BaseConfig.SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    return create_app()
