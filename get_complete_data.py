import pickle

from autotraders.map.waypoint import Waypoint
from autotraders.session import get_session
from tqdm import tqdm

from secret import TOKEN

s = get_session(TOKEN)
all_systems = pickle.load(open("data.pickle", "rb"))

for system in tqdm(all_systems):
    system.waypoints = Waypoint.all(s, str(system.symbol))
pickle.dump(all_systems, open("better_data.pickle", "wb"))
