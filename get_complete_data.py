import pickle
from autotraders.session import get_session
from tqdm import tqdm

from secret import TOKEN

s = get_session(TOKEN)
all_systems = pickle.load(open("data.pickle", "rb"))

for system in tqdm(all_systems):
    system.session = s
    system.update()
pickle.dump(all_systems, open("better_data.pickle", "wb"))
