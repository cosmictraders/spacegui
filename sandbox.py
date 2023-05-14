import time

from autotraders.ship import Ship
from website.session import get_session

s = get_session()
print("Initializing")
starstar2 = Ship("STARSTAR-2", s)
time.sleep(2)
ships = [starstar2]
while True:
    print("Extracting")
    for ship in ships:
        try:
            ship.extract()
        except IOError:
            print("Extracting failed for " + ship.symbol)
        time.sleep(1)
    for ship in ships:
        for i in ship.cargo.inventory:
            print("Selling " + i + " for " + ship.symbol)
            ship.sell(i, ship.cargo.inventory[i])
            time.sleep(0.5)
        time.sleep(3)
    print("Sleeping")
    time.sleep(65)
    # get_system(s, "X1-DF55")