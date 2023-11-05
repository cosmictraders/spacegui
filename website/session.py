from autotraders import session as asession
from flask import session

from website.model import db, Token


def get_session():
    if "username" in session:
        user = db.session.query(Token).filter_by(active=True, user=session["username"]).first()
        if user is None:
            user = db.session.query(Token).filter_by(user=session["username"]).first()
            if user is None:
                return None
            user.active = True
            db.session.commit()
        return asession.AutoTradersSession(user.token)
    else:
        return None


def get_user():
    if "username" in session:
        user = db.session.query(Token).filter_by(user=session["username"]).first()
        return user
    else:
        return None


def login_session(username):
    session["username"] = username
    session["logged_in"] = True


def logout_session():
    del session["username"]
    session["logged_in"] = False


def anonymous_session():
    return asession.AutoTradersSession()
