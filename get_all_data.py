import pickle

from tqdm import tqdm

from autotraders.faction import Faction
from autotraders.map.system import System
from autotraders.session import AutoTradersSession

from secret import TOKEN

print("Starting")
s = AutoTradersSession(TOKEN)
print("Getting Factions")
all_factions = Faction.all(s)
print("Saving Factions")
sanitized = all_factions[1]
for faction in sanitized:
    faction.session = None
pickle.dump(sanitized, open("factions.pickle", "wb"))
print("Getting Systems")
try:
    all_systems = []
    data = s.get(s.b_url + "systems.json").json()
    for jsys in data:
        all_systems.append(System(jsys["symbol"], s, jsys))
    sanitized = all_systems
    for system in sanitized:
        system.session = None
        for waypoint in system.waypoints:
            waypoint.session = None
    pickle.dump(all_systems, open("data.pickle", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
except Exception as e:
    print("Error getting systems from systems.json, getting from api: " + str(e))
    all_systems = System.all(s)
    for i in tqdm(range(1, all_systems.pages + 1)):
        all_systems.next()
    print("Writing ...")
    sanitized = all_systems.stitch()
    for system in sanitized:
        system.session = None
        for waypoint in system.waypoints:
            waypoint.session = None

    pickle.dump(sanitized, open("data.pickle", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
