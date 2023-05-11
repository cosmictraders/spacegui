import time

from main import get_session
from ships import Ship

s = get_session()
while True:
    starstar2 = Ship("STARSTAR-2", s)
    starstar3 = Ship("STARSTAR-3", s)
    print("Extracting")
    try:
        starstar2.extract()
        starstar3.extract()
    except IOError:
        print("Extracting failed")
    time.sleep(1)
    print("Docking")
    starstar2.dock()
    starstar3.dock()
    time.sleep(1)
    print(starstar2.cargo.inventory)
    print(starstar3.cargo.inventory)
    for i in starstar2.cargo.inventory:
        print("Selling " + i)
        starstar2.sell(i, starstar2.cargo.inventory[i])
        time.sleep(0.5)
    time.sleep(1)
    for i in starstar3.cargo.inventory:
        print("Selling " + i)
        starstar3.sell(i, starstar3.cargo.inventory[i])
        time.sleep(0.5)
    print("Refuelling")
    starstar2.refuel()
    time.sleep(1)
    starstar3.refuel()
    time.sleep(1)
    print("Orbiting")
    starstar2.orbit()
    time.sleep(1)
    starstar3.orbit()
    print("Sleeping")
    time.sleep(70)
    # get_system(s, "X1-DF55")