import requests

import secret


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def get_session():
    token = secret.TOKEN

    s = requests.Session()
    s.auth = BearerAuth(token)
    return s
