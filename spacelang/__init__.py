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


class Step:
    def __init__(self, command, data):
        self.command = command
        self.args = data

    def execute(self, ship: Ship, events, session):
        print(self.command)
        if self.command == "move":
            if type(self.args["destination"]) is str:
                ship.navigate(self.command)
            else:
                choices = Waypoint.all(ship.nav.location.system, session)
                ship_current_waypoint = [choice for choice in choices if choice.symbol == ship.nav.location][0]
                tmp = []
                for choice in choices:
                    if "trait" in self.args["destination"]:
                        if len([trait for trait in choice.traits if
                                trait.symbol == self.args["destination"]["trait"]]) != 0:
                            tmp.append(choice)
                    if "type" in self.args["destination"]:
                        if choice.waypoint_type == self.args["destination"]["type"]:
                            tmp.append(choice)
                choices = tmp
                if len(choices) == 0:
                    raise Exception("0 possible waypoints")
                if "selection" not in self.args["destination"] or self.args["destination"][
                    "selection"] == "NEAREST":
                    accepted = choices[0]
                    best = 1000000
                    for choice in choices:
                        if choice.symbol == ship.nav.location:
                            accepted = choice
                            best = -1
                        if math.sqrt(((choice.x-ship_current_waypoint.x) ** 2) + ((choice.y-ship_current_waypoint.y) ** 2)) < best:
                            best = math.sqrt(((choice.x-ship_current_waypoint.x) ** 2) + ((choice.y-ship_current_waypoint.y) ** 2))
                            accepted = choice
                else:
                    accepted = choices[0]
                if str(accepted.symbol) != str(ship.nav.location):
                    ship.navigate(str(accepted.symbol))
                time.sleep(1)
                ship.update()
                if ship.nav.status == "IN_TRANSIT":
                    time.sleep((ship.nav.route.arrival - datetime.now(timezone.utc)).seconds)
        elif self.command == "action":
            repeat_interval = -1
            if type(self.args) is str:
                name = self.args
                repeat = False
            else:
                name = self.args["name"]
                repeat = "repeat" in self.args
                if repeat and "interval" in self.args["repeat"]:
                    repeat_interval = self.args["repeat"]["interval"]
            for event in events:
                if event.name == name:
                    if repeat:
                        if repeat_interval != -1:
                            while True:
                                event.execute(ship, events, session)
                                time.sleep(repeat_interval)
                    else:
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


class Action:
    def __init__(self, name, data):
        self.name = name
        self.actions = []
        for d in data["steps"]:
            if type(d) == str:
                self.actions.append(Step(d, None))
            else:
                self.actions.append(Step(list(d.keys())[0], d[list(d.keys())[0]]))

    def execute(self, ship, events, session):
        for action in self.actions:
            action.execute(ship, events, session)

    def run(self, ships, events, session):
        for ship in ships:
            self.execute(ship, events, session)
            time.sleep(1)


class Trigger:
    def __init__(self, name, data):
        self.name = name  # TODO: Concurrency support
        self.steps = {}
        for group in data:
            self.steps[group] = [Step(d, data[group]["steps"][d]) for d in data[group]["steps"]]

    def run(self, ships, events, session):
        for group in self.steps:
            ship_group = ships[group]
            for ship in ship_group:
                for step in self.steps[group]:
                    step.execute(ship, events, session)


class File:
    def __init__(self, data):
        self.ship_groups = data["ships"]
        self.events = [Action(d, data["actions"][d]) for d in data["actions"]]
        self.triggers = [Trigger(d, data["triggers"][d]) for d in data["triggers"]]

    def run(self, session):
        print("Initializing ship state ...")
        ships = {}
        for group in self.ship_groups:
            ships[group] = [Ship(ship, session) for ship in self.ship_groups[group]]
            time.sleep(0.5)
        contains_onstart = len([trigger for trigger in self.triggers if trigger.name == "on_start"]) == 1
        if contains_onstart:
            on_start = [trigger for trigger in self.triggers if trigger.name == "on_start"][0]
            print("Processing trigger on_start")
            on_start.run(ships, self.events, session)


File(load_text(open("example.yml"))).run(s.get_session(secret.TOKEN))
