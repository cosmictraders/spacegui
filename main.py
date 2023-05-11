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


if __name__ == "__main__":
    s = get_session()
    while True:
        starstar2 = Ship("STARSTAR-2", s)
        starstar3 = Ship("STARSTAR-3", s)
        print("Extracting")
        try:
            starstar2.extract()
            starstar3.extract()
        except IOError:
            print("Extracting failed")
        time.sleep(1)
        print("Docking")
        starstar2.dock()
        starstar3.dock()
        time.sleep(1)
        print(starstar2.cargo.inventory)
        print(starstar3.cargo.inventory)
        for i in starstar2.cargo.inventory:
            print("Selling " + i)
            starstar2.sell(i, starstar2.cargo.inventory[i])
            time.sleep(0.5)
        time.sleep(1)
        for i in starstar3.cargo.inventory:
            print("Selling " + i)
            starstar3.sell(i, starstar3.cargo.inventory[i])
            time.sleep(0.5)
        print("Refuelling")
        starstar2.refuel()
        time.sleep(1)
        starstar3.refuel()
        time.sleep(1)
        print("Orbiting")
        starstar2.orbit()
        time.sleep(1)
        starstar3.orbit()
        print("Sleeping")
        time.sleep(70)
        # get_system(s, "X1-DF55")
