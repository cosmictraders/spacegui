import json
import pickle

from autotraders.map.system import System

data: list[System] = pickle.load(open("data.pickle", "rb"))
data_dict = {}
for i in data:
    waypoints = {}
    for w in i.waypoints:
        traits = []
        if w.traits is not None:
            for trait in w.traits:
                traits.append(trait.symbol)
        waypoints[str(w.symbol)] = {
            "x": w.x,
            "y": w.y,
            "traits": traits,
            "type": w.waypoint_type,
        }
    data_dict[str(i.symbol)] = {
        "type": i.star_type,
        "x": i.x,
        "y": i.y,
        "factions": i.factions,
        "waypoints": waypoints,
        "num_waypoints": len(waypoints),
    }

print(json.dumps(data_dict, indent=4))
