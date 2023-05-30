from flask import *

from autotraders.ship import Ship
from website.session import get_session
from website.wrappers import token_required

ship_bp = Blueprint("ship", __name__)


@ship_bp.route("/ships/")
@token_required
def ships(session):
    li, _ = Ship.all(session)
    return render_template("ships.html", ships=li)


@ship_bp.route("/ship/<name>/")
@token_required
def ship(name, session):
    ship = Ship(name, session)
    return render_template("ship.html", ship=ship)


@ship_bp.route("/ship/<name>/api/")
def ship_api(name):
    s = get_session()
    ship = Ship(name, s)
    return jsonify(
        {
            "symbol": ship.symbol,
            "status": ship.nav.status,
            "location": str(ship.nav.location),
            "fuel": ship.fuel.current,
            "max_fuel": ship.fuel.total,
            "cargo": ship.cargo.inventory,
            "current_cargo": sum(
                [ship.cargo.inventory[d] for d in ship.cargo.inventory]
            ),
            "max_cargo": ship.cargo.capacity,
        }
    )


@ship_bp.route("/ship/<name>/navigate")
def navigate(name):
    try:
        s = get_session()
        ship = Ship(name, s)
        ship.navigate(request.args.get("place"))
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to navigate: " + str(e)})


@ship_bp.route("/ship/<name>/jump")
def jump(name):
    try:
        s = get_session()
        ship = Ship(name, s)
        ship.jump(request.args.get("place"))
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to jump: " + str(e)})


@ship_bp.route("/ship/<name>/warp/")
def warp(name):
    try:
        s = get_session()
        ship = Ship(name, s)
        ship.warp(request.args.get("place"))
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to warp: " + str(e)})


@ship_bp.route("/ship/<name>/dock/")
def dock(name):
    s = get_session()
    ship = Ship(name, s)
    try:
        ship.dock()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to dock: " + str(e)})


@ship_bp.route("/ship/<name>/orbit/")
def orbit(name):
    s = get_session()
    ship = Ship(name, s)
    try:
        ship.orbit()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to orbit: " + str(e)})


@ship_bp.route("/ship/<name>/refuel/")
def refuel(name):
    s = get_session()
    ship = Ship(name, s)
    try:
        ship.refuel()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to refuel: " + str(e)})


@ship_bp.route("/ship/<name>/extract/")
def extract(name):
    s = get_session()
    ship = Ship(name, s)
    try:
        ship.extract()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to extract: " + str(e)})

@ship_bp.route("/ship/<name>/jettison/<symbol>")
def jettison(name, symbol):
    s = get_session()
    ship = Ship(name, s)
    try:
        ship.jettison(symbol, 1)
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Failed to jettison: " + str(e)})
