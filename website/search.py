import difflib
from enum import Enum

from autotraders.ship import Ship


class Condition(Enum):
    LE = -2
    LEQ = -1
    EQ = 0
    GEQ = 1
    GE = 2


class Filter:
    def __init__(self, name, condition):
        self.name = name.strip()
        self.condition_split = [c for c in condition if c != " "]
        self.raw_condition = "".join(self.condition_split)
        if self.raw_condition[0:2] == "<=":
            self.condition = Condition.LEQ
            self.condition_split.pop(0)
            self.condition_split.pop(0)
        elif self.raw_condition[0:2] == ">=":
            self.condition = Condition.GEQ
            self.condition_split.pop(0)
            self.condition_split.pop(0)
        elif self.raw_condition[0:1] == "<":
            self.condition = Condition.LE
            self.condition_split.pop(0)
        elif self.raw_condition[0:1] == ">":
            self.condition = Condition.GE
            self.condition_split.pop(0)
        elif self.raw_condition[0:1] == "=":
            self.condition = Condition.EQ
            self.condition_split.pop(0)
        else:
            self.condition = Condition.EQ
        self.value = ''.join(self.condition_split)

    def validate(self, value):
        if type(value) is str:
            if self.condition == Condition.EQ:
                return value.lower() == self.value.lower()
        elif type(value) is int:
            try:
                if self.condition == Condition.LE:
                    return value < int(self.value)
                elif self.condition == Condition.LEQ:
                    return value <= int(self.value)
                elif self.condition == Condition.EQ:
                    return value == int(self.value)
                elif self.condition == Condition.GEQ:
                    return value >= int(self.value)
                elif self.condition == Condition.GE:
                    return value > int(self.value)
            except ValueError:
                return False
        elif type(value) is float:
            try:
                if self.condition == Condition.LE:
                    return value < float(self.value)
                elif self.condition == Condition.LEQ:
                    return value <= float(self.value)
                elif self.condition == Condition.EQ:
                    return value == float(self.value)
                elif self.condition == Condition.GEQ:
                    return value >= float(self.value)
                elif self.condition == Condition.GE:
                    return value > float(self.value)
            except ValueError:
                return False
        elif type(value) is list:
            if self.condition == Condition.EQ:
                return self.value in [str(item).lower().strip() for item in value]
        else:
            return False


def check_filter_system(system, f: Filter):
    if f.name == "type":
        return f.validate(system.star_type)
    elif f.name == "waypoints":
        return f.validate(len(system.waypoints)) or f.validate(system.waypoints)
    elif f.name == "is":
        return f.validate(["system", "any"])
    elif f.name == "x":
        return f.validate(system.x)
    elif f.name == "y":
        return f.validate(system.y)
    return True


def check_filters_system(system, filters):
    for f in filters:
        if not check_filter_system(system, f):
            return False
    return True


def check_filter_waypoint(waypoint, f: Filter):
    if f.name == "type":
        return f.validate(waypoint.waypoint_type)
    elif f.name == "trait":
        return f.validate(len(waypoint.traits)) or f.validate([trait.symbol for trait in waypoint.traits])
    elif f.name == "is":
        return f.validate(["waypoint", "any"])
    elif f.name == "system":
        return f.validate(waypoint.symbol.system)
    elif f.name == "x":
        return f.validate(waypoint.x)
    elif f.name == "y":
        return f.validate(waypoint.y)
    return True


def check_filters_waypoint(waypoint, filters):
    for f in filters:
        if not check_filter_waypoint(waypoint, f):
            return False
    return True


def check_filter_ship(ship: Ship, f: Filter):
    if f.name == "type":
        return f.validate(ship.registration.role)
    elif f.name == "status":
        return f.validate(ship.nav.status)
    elif f.name == "is":
        return f.validate(["ship", "any"])
    elif f.name == "fuel":
        return f.validate(ship.fuel.current)
    elif f.name == "cargo":
        return f.validate(ship.cargo.current)
    elif f.name == "waypoint":
        return f.validate(ship.nav.location.waypoint)
    elif f.name == "system":
        return f.validate(ship.nav.location.system)
    return True


def check_filters_ship(ship, filters):
    for f in filters:
        if not check_filter_ship(ship, f):
            return False
    return True


def weight(query, s):
    if query.strip() != "":
        weight = difflib.SequenceMatcher(None, query.lower(), s.lower()).ratio()
        return weight * 2 - 1
    else:
        return 0.5


def read_query(q):
    q += " "
    query = ""
    filters = []
    current = ""
    filter_name = None
    filter_condition = None
    in_condition = (
        False  # do we know we are in the condition part (comes after the ":")?
    )
    filter_ending = False  # does next space mean end
    for char in q:
        if char not in [" ", "<", ">", "="] and in_condition:
            filter_ending = True
        if char == ":":
            split = [c for c in current.split(" ") if c != ""]
            if len(split) != 0:
                if len(split) == 1:
                    filter_name = current
                else:
                    filter_name = split.pop()
                    query += " ".join(split)
                current = ""
                in_condition = True
        elif char == " " and filter_ending:
            filter_condition = current
            current = ""
            filter_ending = False
            in_condition = False
            filters.append(Filter(filter_name, filter_condition))
            filter_name = None
            filter_condition = None
            query += " "
        else:
            current += char
    query += current
    return query, filters
