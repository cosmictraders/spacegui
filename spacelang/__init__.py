import math
import time
from datetime import datetime, timezone

import yaml
from autotraders import session as s
from autotraders.map.waypoint import Waypoint
from autotraders.ship import Ship

import secret


def load_text(stream):
    data = yaml.load(stream, Loader=yaml.Loader)
    return data


class Action:
    def __init__(self, data):
        if type(data) is str:
            self.command = data
            self.args = None
        else:
            self.command = list(data.keys())[0]
            self.args = data[self.command]

    def execute(self, ship: Ship, events, session):
        print(self.command)
        if self.command == "move":
            if type(self.args["destination"]) is str:
                ship.navigate(self.command)
            else:
                choices = Waypoint.all(ship.nav.location.system, session)
                tmp = []
                for choice in choices:
                    if "trait" in self.args["destination"][0]:
                        if len([trait for trait in choice.traits if
                                trait.symbol == self.args["destination"][0]["trait"]]) != 0:
                            tmp.append(choice)
                    if "type" in self.args["destination"][0]:
                        if choice.waypoint_type == self.args["destination"][0]["type"]:
                            tmp.append(choice)
                choices = tmp
                if len(choices) == 0:
                    raise Exception("0 possible waypoints")
                if "selection" not in self.args["destination"][0] or self.args["destination"][0]["selection"] == "NEAREST":  # TODO: Fix
                    accepted = choices[0]
                    best = math.sqrt((choices[0].x ** 2) + (choices[0].y ** 2))
                    for choice in choices:
                        if math.sqrt((choice.x ** 2) + (choice.y ** 2)) < best:
                            best = math.sqrt((choice.x ** 2) + (choice.y ** 2))
                            accepted = choice
                else:
                    accepted = choices[0]
                if str(accepted.symbol) != str(ship.nav.location):
                    ship.navigate(str(accepted.symbol))
                time.sleep(3)
                ship.update()
                if ship.nav.status == "IN_TRANSIT":
                    time.sleep((ship.nav.route.arrival - datetime.now(timezone.utc)).seconds)
        elif self.command == "event":
            for event in events:
                if event.name == self.args:
                    event.execute(ship, events, session)
        elif self.command == "orbit":
            ship.orbit()
        elif self.command == "dock":
            ship.dock()
        elif self.command == "refuel":
            ship.refuel()
        elif self.command == "extract":
            ship.extract()
        elif self.command == "sellall":
            for i in ship.cargo.inventory:
                ship.sell(i, ship.cargo.inventory[i])
                time.sleep(0.1)
        elif self.command == "sleep":
            if type(self.args) is int:
                time.sleep(self.args)
            else:
                raise NotImplementedError("TODO")
        else:
            raise NotImplementedError("TODO")
        time.sleep(0.5)


class Runnable:
    def __init__(self, name, data):
        self.name = name
        self.actions = []
        for d in data:
            self.actions.append(Action(d))

    def execute(self, ship, events, session):
        for action in self.actions:
            action.execute(ship, events, session)

    def run(self, ships, events, session):
        for ship in ships:
            self.execute(ship, events, session)
            time.sleep(1)


class File:
    def __init__(self, data):
        self.ships = data["ships"]
        self.events = [Runnable(d, data["events"][d]) for d in data["events"]]
        self.triggers = [Runnable(d, data["triggers"][d]) for d in data["triggers"]]

    def run(self, session):
        print("Initializing ship state ...")
        ships = []
        for ship in self.ships:
            ships.append(Ship(ship, session))
            time.sleep(0.5)
        contains_onstart = len([trigger for trigger in self.triggers if trigger.name == "on_start"]) == 1
        if contains_onstart:
            on_start = [trigger for trigger in self.triggers if trigger.name == "on_start"][0]
            print("Processing trigger on_start")
            on_start.run(ships, self.events, session)


File(load_text(open("example.yml"))).run(s.get_session(secret.TOKEN))
