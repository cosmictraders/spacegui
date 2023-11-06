from autotraders import session as asession
from flask import session

from website.model import db, Token, User


def get_session():
    if "username" in session:
        user = db.session.query(User).filter_by(username=session["username"]).first()
        user_id = user.id
        token = db.session.query(Token).filter_by(active=True, user=user_id).first()
        if token is None:
            token = db.session.query(Token).filter_by(user=user_id).first()
            if token is None:
                return None
            token.active = True
            db.session.commit()
        return asession.AutoTradersSession(token.token)
    else:
        return None


def get_user():
    if "username" in session:
        user = db.session.query(User).filter_by(username=session["username"]).first()
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
