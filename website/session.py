from autotraders import session

from website.model import db, User


def get_session():
    user = db.session.query(User).filter_by(active=True).first()
    t = user.token
    return session.get_session(t)
