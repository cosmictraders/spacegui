from contract import Contract
from ships import Ship


class Agent:
    def __init__(self, session):
        self.session = session
        self.update()

    def update(self):
        r = self.session.get("https://api.spacetraders.io/v2/my/agent")
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.account_id = j["data"]["accountId"]
        self.symbol = j["data"]["symbol"]
        self.headquarters = j["data"]["headquarters"]
        self.credits = j["data"]["credits"]
        r = self.session.get("https://api.spacetraders.io/v2/my/ships")
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.ships = []
        for ship in j["data"]:
            s = Ship(ship["symbol"], self.session, False)
            s.update(ship)
            self.ships.append(s)
        r = self.session.get("https://api.spacetraders.io/v2/my/contracts")
        j = r.json()
        self.contracts = []
        for contract in j["data"]:
            c = Contract(contract["id"], self.session, False)
            c.update(contract)
            self.contracts.append(c)