from autotraders import session

from website.model import db, User


def get_session():
    user = db.session.query(User).filter_by(active=True).first()
    return session.AutoTradersSession(user.token)

def get_token():
    user = db.session.query(User).filter_by(active=True).first()
    return user.token
