import time

from autotraders import session
from autotraders.ship import Ship

import secret

s = session.get_session(secret.TOKEN)
print("Initializing")
starstar2 = Ship("STARSTAR-2", s)
time.sleep(2)
ships = [starstar2]
while True:
    print("Orbiting")
    for ship in ships:
        ship.orbit()
    print("Extracting")
    for ship in ships:
        try:
            ship.extract()
        except IOError as e:
            print("Extracting failed for " + ship.symbol + " because " + str(e))
        time.sleep(1)
    print("Checking to sell")
    for ship in ships:
        print("Cargo for " + ship.symbol + ": " + str(ship.cargo.inventory))
        for i in ship.cargo.inventory:
            print("Selling " + i + " for " + ship.symbol)
            ship.sell(i, ship.cargo.inventory[i])
            time.sleep(0.5)
        time.sleep(3)
    print("Sleeping")
    time.sleep(65)
    # get_system(s, "X1-DF55")