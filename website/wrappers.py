import autotraders.token
from flask import redirect, url_for, flash, session

from website.session import get_session, get_user


def minify_html(func):
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        # TODO: minify HTML output
        return result

    wrap.__name__ = func.__name__
    wrap.__doc__ = func.__doc__
    return wrap


def token_required(func):
    def wrap(*args, **kwargs):
        session = get_session()
        if session is None:
            return redirect(url_for("local.select_token"))
        result = func(*args, **kwargs, session=session)
        return result

    wrap.__name__ = func.__name__
    wrap.__doc__ = func.__doc__
    return wrap


def login_required(func):
    def wrap(*args, **kwargs):
        user = get_user()
        if user is None:
            flash("Not logged in", "danger")
            return redirect(url_for("auth.login"))
        result = func(*args, **kwargs, user=user)
        return result

    wrap.__name__ = func.__name__
    wrap.__doc__ = func.__doc__
    return wrap
