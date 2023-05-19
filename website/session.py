from autotraders import session

from website.model import db, User


def get_session():
    user = db.session.execute(db.select(User)).first()[0]
    t = user.token
    return session.get_session(t)
