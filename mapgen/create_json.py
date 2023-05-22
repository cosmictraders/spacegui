import inspect
import json
import pickle

data = pickle.load(open("data.pickle", "rb"))
data_dict = {}
for i in data:  # TODO: Waypoints
    data_dict[i.symbol] = {
        "type": i.star_type,
        "x": i.x,
        "y": i.y,
        "factions": i.factions,
    }
print(json.dumps(data_dict, indent=4))
