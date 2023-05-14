from flask import *

from autotraders.ship import Ship, get_all_ships
from website.session import get_session

ship_bp = Blueprint('ship', __name__)


@ship_bp.route('/ships/')
def ships():
    s = get_session()
    li = get_all_ships(s)
    return render_template('ships.html', ships=li)


@ship_bp.route('/ship/<name>')
def ship(name):
    return render_template('ship.html', symbol=name)


@ship_bp.route('/ship/<name>/api')
def ship_api(name):
    s = get_session()
    ship = Ship(name, s)
    return jsonify({"symbol": ship.symbol, "status": ship.nav.status, "location": ship.nav.location,
                    "fuel": ship.fuel.current, "max_fuel": ship.fuel.total,
                    "cargo": ship.cargo.inventory,
                    "current_cargo": sum([ship.cargo.inventory[d] for d in ship.cargo.inventory]),
                    "max_cargo": ship.cargo.capacity})


@ship_bp.route('/ship/<name>/navigate')
def navigate(name):
    try:
        s = get_session()
        ship = Ship(name, s)
        ship.move(request.args.get('place'))
        return jsonify({})
    except IOError as e:
        return jsonify({"error": "Unknown"})


@ship_bp.route('/ship/<name>/jump')
def jump(name):
    try:
        s = get_session()
        ship = Ship(name, s)
        ship.jump(request.args.get('place'))
        return jsonify({})
    except IOError as e:
        abort(500)


@ship_bp.route('/ship/<name>/warp')
def warp(name):
    try:
        s = get_session()
        ship = Ship(name, s)
        ship.warp(request.args.get('place'))
        return jsonify({})
    except IOError:
        abort(500)


@ship_bp.route('/ship/<name>/dock')
def dock(name):
    s = get_session()
    ship = Ship(name, s)
    try:
        ship.dock()
        return jsonify({})
    except IOError:
        return jsonify({"error": "Failed to dock"})


@ship_bp.route('/ship/<name>/orbit')
def orbit(name):
    s = get_session()
    ship = Ship(name, s)
    ship.orbit()
    return jsonify({})


@ship_bp.route('/ship/<name>/refuel')
def refuel(name):
    s = get_session()
    ship = Ship(name, s)
    ship.refuel()
    return jsonify({})


@ship_bp.route('/ship/<name>/extract')
def extract(name):
    s = get_session()
    ship = Ship(name, s)
    ship.extract()
    return jsonify({})
