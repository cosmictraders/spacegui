import json
import pickle
import random

from autotraders.map.system import System

data: list[System] = pickle.load(open("data.pickle", "rb"))
data_dict = {}
for i in data:  # TODO: Waypoints
    waypoints = {}
    for w in i.waypoints:
        traits = []
        for trait in w.traits:
            traits.append(trait.symbol)
        waypoints[str(w.symbol)] = {"x": w.x, "y": w.y, "traits": traits, "type": w.waypoint_type}
    data_dict[str(i.symbol)] = {
        "type": i.star_type,
        "x": i.x,
        "y": i.y,
        "factions": i.factions,
        "waypoints": []
    }

print(json.dumps(data_dict, indent=4))
