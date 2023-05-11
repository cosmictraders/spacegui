import time

import requests

import secret
from ships import *
from system import System


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def list_systems(session) -> list[System]:
    r = session.get("https://api.spacetraders.io/v2/systems?limit=20")
    j = r.json()["data"]
    systems = []
    for system in j:
        s = System(system["symbol"], session, False)
        s.update(system)
        systems.append(s)
    return systems


def list_waypoints(session, system):
    print("System: " + system)
    r = session.get("https://api.spacetraders.io/v2/systems/" + system + "/waypoints")
    j = r.json()
    for waypoint in j["data"]:
        print(waypoint["symbol"] + ": " + waypoint["type"])
    print(j)


def accept_contract(session, contract_id):
    r = session.post("https://api.spacetraders.io/v2/my/contracts/" + contract_id + "/accept")
    print(r.text)


def get_session():
    token = secret.TOKEN

    s = requests.Session()
    s.auth = BearerAuth(token)
    return s
