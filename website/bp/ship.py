from datetime import datetime, timezone

from flask import *

from autotraders.ship import Ship
from website.session import get_session
from website.wrappers import token_required, minify_html

ship_bp = Blueprint("ship", __name__)


@ship_bp.route("/ships/")
@minify_html
@token_required
def ships(session):
    li = Ship.all(session)
    return render_template("ship/ships.html", ships=li)


@ship_bp.route("/ship/<name>/")
@minify_html
@token_required
def ship(name, session):
    ship = Ship(name, session)
    j = json.load(open("./website/static/systems.json"))
    li: list[str] = list(j.keys())
    waypoints_raw = j[ship.nav.location.system]["waypoints"]
    waypoints = [
        f'{waypoint} ({waypoints_raw[waypoint]["type"]})' for waypoint in waypoints_raw
    ]
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
    li: list[str] = list(j.keys())
    waypoints_raw = j[ship.nav.location.system]["waypoints"]
    waypoints = [
        f'{waypoint} ({waypoints_raw[waypoint]["type"]})' for waypoint in waypoints_raw
    ]
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
        ship = Ship(name, s)
        if ship.nav.flight_mode != request.args.get("mode", ship.nav.flight_mode):
            ship.patch_navigation(request.args.get("mode", ship.nav.flight_mode))
        ship.navigate(request.args.get("place"))
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to navigate: " + str(e)})


@ship_bp.route("/ship/<name>/jump")
def jump(name):
    try:
        s = get_session()
        ship = Ship(name, s, data={})
        ship.jump(request.args.get("place"))
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to jump: " + str(e)})


@ship_bp.route("/ship/<name>/warp/")
def warp(name):
    try:
        s = get_session()
        ship = Ship(name, s, data={})
        ship.warp(request.args.get("place"))
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to warp: " + str(e)})


@ship_bp.route("/ship/<name>/dock/")
def dock(name):
    s = get_session()
    ship = Ship(name, s, data={})
    try:
        ship.dock()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to dock: " + str(e)})


@ship_bp.route("/ship/<name>/orbit/")
def orbit(name):
    s = get_session()
    ship = Ship(name, s, data={})
    try:
        ship.orbit()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to orbit: " + str(e)})


@ship_bp.route("/ship/<name>/refuel/")
def refuel(name):
    s = get_session()
    ship = Ship(name, s, data={})
    try:
        ship.refuel()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to refuel: " + str(e)})


@ship_bp.route("/ship/<name>/extract/")
def extract(name):
    s = get_session()
    ship = Ship(name, s, data={})
    try:
        ship.extract()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to extract: " + str(e)})


@ship_bp.route("/ship/<name>/jettison/<symbol>")
def jettison(name, symbol):
    s = get_session()
    ship = Ship(name, s, data={})
    try:
        ship.jettison(symbol, 1)
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to jettison: " + str(e)})


@ship_bp.route("/ship/<name>/transfer/<symbol>")
def transfer(name, symbol):
    s = get_session()
    ship = Ship(name, s, data={})
    try:
        ship.jettison(symbol, 1)
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to transfer cargo: " + str(e)})


@ship_bp.route("/ship/<name>/sell/<symbol>")
def sell(name, symbol):
    s = get_session()
    ship = Ship(name, s, data={})
    try:
        ship.jettison(symbol, 1)
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to sell: " + str(e)})
