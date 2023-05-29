import math

from autotraders.map.waypoint_types.marketplace import Marketplace
from autotraders.map.waypoint_types.shipyard import Shipyard
from autotraders.map.system import System
from autotraders.map.waypoint import get_all_waypoints, Waypoint
from flask import *

from website.session import get_session
from website.wrappers import token_required

system_bp = Blueprint("system", __name__)


@system_bp.route("/systems/")
@token_required
def systems(session):
    page = int(request.args.get("page", default=1))
    systems_list, total = System.all(session, page)
    total = math.ceil((total / 20))
    li = {1, 2, 3, 4, 5, total - 2, total - 1, total}
    li.add(page)
    if page > min(li):
        li.add(page - 1)
    if page < max(li):
        li.add(page + 1)
    li = list(li)
    li.sort()
    new_li = []
    prev = 0
    for i in li:
        if i != (prev + 1):
            new_li.append("..")
        new_li.append(i)
        prev = i
    return render_template(
        "systems.html", systems=systems_list, page=page, pages=total, li=new_li
    )


@system_bp.route("/system/<symbol>/")
def system(symbol):
    s = get_session()
    return render_template(
        "system.html",
        system=System(symbol, s),
        waypoints=get_all_waypoints(symbol, s)[0],
    )


@system_bp.route("/waypoint/<symbol>/")
def waypoint(symbol):
    w = Waypoint(symbol, get_session())
    if w.marketplace:
        m = Marketplace(symbol, get_session())
    else:
        m = None
    if w.shipyard:
        s = Shipyard(symbol, get_session())
    else:
        s = None
    return render_template("waypoint.html", waypoint=w, marketplace=m, shipyard=s)


@system_bp.route("/waypoint/<symbol>/buy-ship/")
def buy_ship(symbol):
    w = Waypoint(symbol, get_session())
    if w.shipyard:
        s = Shipyard(symbol, get_session())
        s.purchase(request.args.get("ship"))
        return jsonify({})
    else:
        abort(404)
