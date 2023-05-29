from flask import render_template

from website.model import db
from website.session import get_session


def minify(func):
    raise NotImplementedError("")


def token_required(func):
    """Decorator that reports the execution time."""

    def wrap(*args, **kwargs):
        try:
            session = get_session()
            result = func(*args, **kwargs, session=session)
            return result
        except Exception as e:
            print(e)
            db.create_all()
            return render_template("setup.html")
    return wrap