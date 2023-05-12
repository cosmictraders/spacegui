import time

from flask import *

from autotraders.contract import get_all_contracts
from bp.ship import ship_bp
from autotraders.agent import Agent
from autotraders.contract import Contract
from autotraders.waypoint import Waypoint, get_all_waypoints
from session import get_session
from autotraders.system import list_systems, System

app = Flask(__name__)

app.register_blueprint(ship_bp)


@app.route('/')
def index():
    s = get_session()
    agent = Agent(s)
    return render_template('index.html', agent=agent)


@app.route('/contracts/')
def contracts():
    s = get_session()
    return render_template('contracts.html', contracts=get_all_contracts(s))


@app.route('/contract/<contract_id>')
def contract(contract_id):
    s = get_session()
    return render_template('contract.html', contract=Contract(contract_id, s))


@app.route('/contract/<contract_id>/accept')
def accept_contract(contract_id: str):
    s = get_session()
    c = Contract(contract_id, s)
    c.accept()
    return jsonify({})


@app.route('/systems/')
def systems():
    page = request.args.get('page', default=1)
    systems_list, total = list_systems(get_session(), page)
    return render_template('systems.html', systems=systems_list,
                           page=int(page), pages=total)


@app.route('/system/<symbol>/')
def system(symbol):
    return render_template("system.html", system=System(symbol, get_session()),
                           waypoints=get_waypoints(symbol, get_session()))


@app.route('/waypoint/<symbol>/')
def waypoint(symbol):
    return render_template("waypoint.html", waypoint=Waypoint(symbol, get_session()))


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
