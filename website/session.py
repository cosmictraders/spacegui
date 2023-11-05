from autotraders import session as asession
from flask import session

from website.model import db, Token


def get_session():
    if session["username"] is not None:
        user = db.session.query(Token).filter_by(active=True, username=session["username"]).first()
        if user is None:
            user = db.session.query(Token, username=session["username"]).first()
            if user is None:
                raise ValueError("No token not found")
            user.active = True
            db.session.commit()
        return asession.AutoTradersSession(user.token)
    else:
        raise ValueError("User not logged in")


def get_user():
    if session["username"] is not None:
        user = db.session.query(Token).filter_by(username=session["username"]).first()
        return user
    else:
        raise ValueError("User not logged in")


def login_session(username):
    session["username"] = username
    session["logged_in"] = True


def logout_session():
    del session["username"]
    session["logged_in"] = False
