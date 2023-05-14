from autotraders import session

import secret


def get_session():
    token = secret.TOKEN
    return session.get_session(token)
