import time

from sdk.ships import Ship
from session import get_session

s = get_session()
print("Initializing")
starstar2 = Ship("STARSTAR-2", s)
time.sleep(2)
starstar3 = Ship("STARSTAR-3", s)
time.sleep(2)
starstar4 = Ship("STARSTAR-4", s)
time.sleep(2)
starstar6 = Ship("STARSTAR-6", s)
time.sleep(2)
starstar7 = Ship("STARSTAR-7", s)
time.sleep(2)
ships = [starstar2, starstar3, starstar4, starstar6, starstar7]
while True:
    print("Extracting")
    for ship in ships:
        try:
            ship.extract()
        except IOError:
            print("Extracting failed for " + ship.symbol)
        time.sleep(1)
    print("Docking")
    for ship in ships:
        ship.dock()
        time.sleep(1)
    for ship in ships:
        for i in ship.cargo.inventory:
            print("Selling " + i + " for " + ship.symbol)
            ship.sell(i, ship.cargo.inventory[i])
            time.sleep(0.5)
        time.sleep(3)
    print("Refuelling")
    for ship in ships:
        ship.refuel()
        time.sleep(1)
    print("Orbiting")
    for ship in ships:
        ship.orbit()
        time.sleep(1)
    print("Sleeping")
    time.sleep(60)
    # get_system(s, "X1-DF55")