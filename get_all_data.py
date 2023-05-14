import pickle
import time
from tqdm import tqdm
from autotraders.system import list_systems

from website.session import get_session

s = get_session()
all_systems = []
for i in tqdm(range(1, 250)):
    for item in list_systems(s, i)[0]:
        all_systems.append(item)
    time.sleep(1)
print("Writing ...")
pickle.dump(all_systems, open("data.pickle", "wb"))
