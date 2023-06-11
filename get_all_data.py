import pickle
from tqdm import tqdm
from autotraders.map.system import System

from autotraders.session import get_session

from secret import TOKEN

s = get_session(TOKEN)
all_systems = System.all(s)
for i in tqdm(range(1, all_systems.pages+1)):
    all_systems.next()
print("Writing ...")
pickle.dump(all_systems.stitch(), open("data.pickle", "wb"))
all_systems_stitch = all_systems.stitch()
for system in all_systems:
    system.update()
pickle.dump(all_systems.stitch(), open("better_data.pickle", "wb"))
