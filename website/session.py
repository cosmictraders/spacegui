from autotraders import session

from website.model import db, User


def get_session():
    user = db.session.query(User).filter_by(active=True).first()
    if user is None:
        user = db.session.query(User).first()
        user.active = True
        db.session.commit()
    return session.AutoTradersSession(user.token)


def get_token():
    user = db.session.query(User).filter_by(active=True).first()
    return user.token
