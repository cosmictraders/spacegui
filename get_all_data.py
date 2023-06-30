import pickle

from autotraders.faction import Faction
from tqdm import tqdm
from autotraders.map.system import System

from autotraders.session import get_session

from secret import TOKEN

s = get_session(TOKEN)
all_factions = Faction.all(s)
pickle.dump(all_factions[1], open("factions.pickle", "wb"))
all_systems = System.all(s)
for i in tqdm(range(1, all_systems.pages + 1)):
    all_systems.next()
print("Writing ...")
pickle.dump(all_systems.stitch(), open("data.pickle", "wb"))
