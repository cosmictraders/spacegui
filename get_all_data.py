import pickle
import time
from tqdm import tqdm
from autotraders.map.system import list_systems

from autotraders.session import get_session

from secret import TOKEN

s = get_session(TOKEN)
all_systems = []
for i in tqdm(range(1, 500)):
    for item in list_systems(s, i)[0]:
        all_systems.append(item)
    time.sleep(1)
print("Writing ...")
pickle.dump(all_systems, open("data.pickle", "wb"))
