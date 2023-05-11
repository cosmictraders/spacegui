import time

from flask import *

from agent import Agent
from main import *
from waypoint import get_waypoints

app = Flask(__name__)


@app.route('/')
def index():
    s = get_session()
    agent = Agent(s)
    return render_template('index.html', agent=agent)


@app.route('/contracts/')
def contracts():
    s = get_session()
    agent = Agent(s)
    return render_template('contracts.html', contracts=agent.contracts)


@app.route('/contract/<contract_id>')
def contract(contract_id):
    s = get_session()
    r = s.get("https://api.spacetraders.io/v2/my/contracts")
    j = r.json()
    return render_template('contract.html', contract=j["data"])


@app.route('/ships/')
def ships():
    s = get_session()
    li = [Ship("STARSTAR-1", s), Ship("STARSTAR-2", s), Ship("STARSTAR-3", s)]  # TODO: Don't hardcode
    return render_template('ships.html', ships=li)


@app.route('/ship/<name>')
def ship(name):
    return render_template('ship.html', symbol=name)


@app.route('/ship/<name>/api')
def ship_api(name):
    s = get_session()
    ship = Ship(name, s)
    return jsonify({"symbol": ship.symbol, "status": ship.status, "location": ship.location,
                    "fuel": ship.fuel.current, "max_fuel": ship.fuel.total})


@app.route('/ship/<name>/navigate')
def navigate(name):
    try:
        s = get_session()
        ship = Ship(name, s)
        ship.move(request.args.get('place'))
        return jsonify({})
    except IOError:
        abort(500)


@app.route('/ship/<name>/dock')
def dock(name):
    s = get_session()
    ship = Ship(name, s)
    ship.dock()
    return jsonify({})


@app.route('/ship/<name>/orbit')
def orbit(name):
    s = get_session()
    ship = Ship(name, s)
    ship.orbit()
    return jsonify({})


@app.route('/ship/<name>/refuel')
def refuel(name):
    s = get_session()
    ship = Ship(name, s)
    ship.refuel()
    return jsonify({})


@app.route('/systems/')
def systems():
    print("here")
    return render_template('systems.html', systems=list_systems(get_session()))


@app.route('/system/<symbol>/')
def system(symbol):
    return render_template("system.html", system=System(symbol, get_session()),
                           waypoints=get_waypoints(symbol, get_session()))


@app.route('/map/')
def map():
    s = get_session()
    r = s.get("https://api.spacetraders.io/v2/systems?limit=20")
    r2 = s.get("https://api.spacetraders.io/v2/systems?limit=20&page=2")
    time.sleep(2)
    r3 = s.get("https://api.spacetraders.io/v2/systems?limit=20&page=3")
    time.sleep(2)
    r4 = s.get("https://api.spacetraders.io/v2/systems?limit=20&page=3")
    j = r.json()
    j1 = r2.json()
    j2 = r3.json()
    j3 = r4.json()
    systems = []
    for system_json in j["data"]:
        systems.append("[" + str(system_json["x"]) + "," + str(system_json["y"]) + "]")
    for system_json in j1["data"]:
        systems.append("[" + str(system_json["x"]) + "," + str(system_json["y"]) + "]")
    for system_json in j2["data"]:
        systems.append("[" + str(system_json["x"]) + "," + str(system_json["y"]) + "]")
    for system_json in j3["data"]:
        systems.append("[" + str(system_json["x"]) + "," + str(system_json["y"]) + "]")
    return render_template('map.html', coords="[" + ",".join(systems) + "]")


if __name__ == '__main__':
    app.run(debug=True)
