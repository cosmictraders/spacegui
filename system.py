from waypoint import Waypoint


class System:
    def __init__(self, symbol, session, update=True):
        self.session = session
        self.symbol = symbol
        self.waypoints = []
        if update:
            self.update()

    def update(self, data=None):
        if data is None:
            r = self.session.get("https://api.spacetraders.io/v2/systems/" + self.symbol)
            data = r.json()["data"]
        self.waypoints = []
        self.x = data["x"]
        self.y = data["y"]
        self.factions = data["factions"]
        for w in data["waypoints"]:
            waypoint = Waypoint(w["symbol"], self.session, False)
            waypoint.update(w)
            self.waypoints.append(waypoint)
