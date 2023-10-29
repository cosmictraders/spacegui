from datetime import datetime, timezone

from autotraders.error import SpaceTradersException
from flask import *

from autotraders.ship import Ship

from website.paginated_return import paginated_return
from website.session import get_session
from website.wrappers import token_required, minify_html

ship_bp = Blueprint("ship", __name__)


@ship_bp.route("/ships/")
@minify_html
@token_required
def ships(session):
    page = int(request.args.get("page", default=1))
    ships = Ship.all(session, page)
    new_li = paginated_return(ships, page)
    return render_template("ship/ships.html", ships=ships, page=page, li=new_li)


@ship_bp.route("/ships/api-json/")
def ships_json_api():
    s = get_session()
    ships = Ship.all(s, 1)[1]
    li_json = []
    for ship in ships:
        li_json.append({
            "symbol": ship.symbol,
            "role": ship.registration.role,
            "nav": {
                "location": str(ship.nav.location),
                "status": ship.nav.status,
                "flight_mode": ship.nav.flight_mode,
            }
        })
    return jsonify(li_json)


@ship_bp.route("/ship/<name>/")
@minify_html
@token_required
def ship(name, session):
    ship = Ship(name, session)
    j = json.load(open("./website/static/systems.json"))
    li: list[tuple[str, str]] = [(i, i) for i in list(j.keys())]
    try:
        waypoints_raw = j[ship.nav.location.system]["waypoints"]
        waypoints = [
            (waypoint, f'{waypoint} ({waypoints_raw[waypoint]["type"]})')
            for waypoint in waypoints_raw
        ]
    except:
        waypoints = []
    return render_template(
        "ship/ship.html",
        ship=ship,
        waypoint_options=waypoints + li,
        now=datetime.now(timezone.utc),
    )


@ship_bp.route("/ship/<name>/api/")
def ship_api(name):
    s = get_session()
    ship = Ship(name, s)
    j = json.load(open("./website/static/systems.json"))
    li: list[tuple[str, str]] = [(i, i) for i in list(j.keys())]
    try:
        waypoints_raw = j[ship.nav.location.system]["waypoints"]
        waypoints = [
            (waypoint, f'{waypoint} ({waypoints_raw[waypoint]["type"]})')
            for waypoint in waypoints_raw
        ]
    except:
        waypoints = []
    return render_template(
        "ship/ship_api.html",
        ship=ship,
        waypoint_options=waypoints + li,
        now=datetime.now(timezone.utc),
    )


@ship_bp.route("/ship/<name>/navigate")
def navigate(name):
    try:
        s = get_session()
        ship = Ship(name, s)  # TODO: Fix extra api request
        if ship.nav.flight_mode != request.args.get("mode", ship.nav.flight_mode):
            ship.patch_navigation(request.args.get("mode", ship.nav.flight_mode))
        ship.navigate(request.args.get("place").strip())
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to navigate: " + str(e)})


@ship_bp.route("/ship/<name>/jump")
def jump(name):
    try:
        s = get_session()
        ship = Ship(name, s)  # TODO: Fix extra api request
        ship.jump(request.args.get("place").strip())
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to jump: " + str(e)})


@ship_bp.route("/ship/<name>/warp/")
def warp(name):
    try:
        s = get_session()
        ship = Ship(name, s)  # TODO: Fix extra api request
        ship.warp(request.args.get("place").strip())
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to warp: " + str(e)})


@ship_bp.route("/ship/<name>/dock/")
def dock(name):
    s = get_session()
    ship = Ship(name, s)  # TODO: Fix extra api request
    try:
        ship.dock()
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to dock: " + str(e)})


@ship_bp.route("/ship/<name>/orbit/")
def orbit(name):
    s = get_session()
    ship = Ship(name, s)  # TODO: Fix extra api request
    try:
        ship.orbit()
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to orbit: " + str(e)})


@ship_bp.route("/ship/<name>/refuel/")
def refuel(name):
    s = get_session()
    ship = Ship(name, s)  # TODO: Fix extra api request
    try:
        ship.refuel()
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to refuel: " + str(e)})


@ship_bp.route("/ship/<name>/extract/")
def extract(name):
    s = get_session()
    ship = Ship(name, s)  # TODO: Fix extra api request
    try:
        ship.extract()
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to extract: " + str(e)})


@ship_bp.route("/ship/<name>/siphon/")
def siphon(name):
    s = get_session()
    ship = Ship(name, s)  # TODO: Fix extra api request
    try:
        ship.siphon()
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to siphon: " + str(e)})


@ship_bp.route("/ship/<name>/chart/")
def chart(name):
    s = get_session()
    ship = Ship(
        name,
        s
    )  # TODO: Fix extra api request
    try:
        ship.chart()
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to chart: " + str(e)})


@ship_bp.route("/ship/<name>/jettison/<symbol>/<quantity>")
def jettison(name, symbol, quantity):
    s = get_session()
    ship = Ship(name, s, data={"modules": {}, "mounts": {}})
    try:
        ship.jettison(symbol, quantity)
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to jettison: " + str(e)})


@ship_bp.route("/ship/<name>/transfer/<symbol>/<quantity>")
def transfer(name, symbol, quantity):
    s = get_session()
    ship = Ship(name, s, data={"modules": {}, "mounts": {}})
    try:
        ship.jettison(symbol, quantity)
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to transfer cargo: " + str(e)})


@ship_bp.route("/ship/<name>/buy/<symbol>/<quantity>")
def buy(name, symbol, quantity):
    s = get_session()
    ship = Ship(name, s, data={"modules": {}, "mounts": {}})
    try:
        ship.buy(symbol, quantity)
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to sell: " + str(e)})


@ship_bp.route("/ship/<name>/sell/<symbol>/<quantity>")
def sell(name, symbol, quantity):
    s = get_session()
    ship = Ship(name, s, data={"modules": {}, "mounts": {}})
    try:
        ship.sell(symbol, quantity)
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to sell: " + str(e)})


@ship_bp.route("/ship/<name>/scan-ships/")
def scan_ships(name):
    s = get_session()
    ship = Ship(name, s)  # TODO: Fix extra api request
    resp = ship.scan_ships()
    return render_template("ship/scan_ships.html", ships=resp)


@ship_bp.route("/ship/<name>/scan-waypoints/")
def scan_waypoints(name):
    s = get_session()  # TODO: Fix extra api request
    ship = Ship(name, s)
    resp = ship.scan_waypoints()
    return render_template("ship/scan_waypoints.html", waypoints=resp)


@ship_bp.route("/ship/<name>/scan-systems/")
def scan_systems(name):
    s = get_session()  # TODO: Fix extra api request
    ship = Ship(name, s)
    resp = ship.scan_systems()
    return render_template("ship/scan_systems.html", waypoints=resp)


@ship_bp.route("/ships/fitting-manager")
def fitting_manager():
    return render_template("ship/fitting_manager.html")
