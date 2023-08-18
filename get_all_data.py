import pickle

from autotraders.faction import Faction
from tqdm import tqdm
from autotraders.map.system import System

from autotraders.session import get_session

from secret import TOKEN

print("Starting")
s = get_session(TOKEN)
print("Getting Factions")
all_factions = Faction.all(s)
print("Saving Factions")
pickle.dump(all_factions[1], open("factions.pickle", "wb"))
print("Getting Systems")
try:
    all_systems = []
    data = s.get(s.base_url + "systems.json").json()
    for jsys in data:
        all_systems.append(System(jsys["symbol"], s, jsys))
    pickle.dump(all_systems, open("data.pickle", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
except:
    all_systems = System.all(s)
    for i in tqdm(range(1, all_systems.pages + 1)):
        all_systems.next()
    print("Writing ...")
    pickle.dump(all_systems.stitch(), open("data.pickle", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
