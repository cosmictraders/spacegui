from datetime import datetime, timezone

from autotraders.error import SpaceTradersException
from flask import *

from autotraders.ship import Ship
from website.session import get_session
from website.wrappers import token_required, minify_html

ship_bp = Blueprint("ship", __name__)


@ship_bp.route("/ships/")
@minify_html
@token_required
def ships(session):
    page = int(request.args.get("page", default=1))
    ships = Ship.all(session, page)
    li = {
        1
    }
    if ships.pages > 1:
        li.add(2)
        if ships.pages > 2:
            li.add(3)
            if ships.pages > 3:
                li.add(4)
                if ships.pages > 4:
                    li.add(5)
    if ships.pages > 0:
        li.add(ships.pages - 2)
    if ships.pages > 0:
        li.add(ships.pages - 1)
    if ships.pages > 0:
        li.add(ships.pages)
    li = list(li)
    li.sort()
    new_li = []
    prev = 0
    for i in li:
        if i != (prev + 1):
            new_li.append("..")
        new_li.append(i)
        prev = i
    return render_template("ship/ships.html", ships=ships, page=page, li=new_li)


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
        ship = Ship(name, s)
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
        ship = Ship(name, s, data={"modules": {}, "mounts": {}})
        ship.jump(request.args.get("place").strip())
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to jump: " + str(e)})


@ship_bp.route("/ship/<name>/warp/")
def warp(name):
    try:
        s = get_session()
        ship = Ship(name, s, data={"modules": {}, "mounts": {}})
        ship.warp(request.args.get("place").strip())
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to warp: " + str(e)})


@ship_bp.route("/ship/<name>/dock/")
def dock(name):
    s = get_session()
    ship = Ship(name, s, data={"modules": {}, "mounts": {}})
    try:
        ship.dock()
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to dock: " + str(e)})


@ship_bp.route("/ship/<name>/orbit/")
def orbit(name):
    s = get_session()
    ship = Ship(name, s, data={"modules": {}, "mounts": {}})
    try:
        ship.orbit()
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to orbit: " + str(e)})


@ship_bp.route("/ship/<name>/refuel/")
def refuel(name):
    s = get_session()
    ship = Ship(name, s, data={"modules": {}, "mounts": {}})
    try:
        ship.refuel()
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to refuel: " + str(e)})


@ship_bp.route("/ship/<name>/extract/")
def extract(name):
    s = get_session()
    ship = Ship(
        name,
        s,
        data={
            "modules": {},
            "mounts": {},
            "reactor": {
                "symbol": "blank",
                "name": "blank",
                "powerOutput": 1,
                "cooldown": "2000-01-01 00:00:00.000",
                "requirements": {},
            },
        },
    )
    try:
        ship.extract()
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to extract: " + str(e)})


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


@ship_bp.route("/ship/<name>/sell/<symbol>/<quantity>")
def sell(name, symbol, quantity):
    s = get_session()
    ship = Ship(name, s, data={"modules": {}, "mounts": {}})
    try:
        ship.sell(symbol, quantity)
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": "Failed to sell: " + str(e)})
