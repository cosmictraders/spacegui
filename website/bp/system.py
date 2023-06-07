import math

from autotraders.map.waypoint_types.marketplace import Marketplace
from autotraders.map.waypoint_types.shipyard import Shipyard
from autotraders.map.system import System
from autotraders.map.waypoint import Waypoint
from flask import *

from website.wrappers import token_required, minify_html

system_bp = Blueprint("system", __name__)


@system_bp.route("/systems/")
@minify_html
@token_required
def systems(session):
    page = int(request.args.get("page", default=1))
    systems_list = System.all(session, page)
    li = {1, 2, 3, 4, 5, systems_list.pages - 2, systems_list.pages - 1, systems_list.pages}
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
        "map/systems.html", systems=systems_list, li=new_li
    )


@system_bp.route("/system/<symbol>/")
@minify_html
@token_required
def system(symbol, session):
    waypoints = Waypoint.all(session, symbol)
    return render_template(
        "map/system.html",
        system=System(symbol, session),
        waypoints=waypoints[1],
    )


@system_bp.route("/waypoint/<symbol>/")
@minify_html
@token_required
def waypoint(symbol, session):
    w = Waypoint(symbol, session)
    if w.marketplace:
        m = Marketplace(symbol, session)
    else:
        m = None
    if w.shipyard:
        s = Shipyard(symbol, session)
    else:
        s = None
    return render_template("map/waypoint.html", waypoint=w, marketplace=m, shipyard=s)


@system_bp.route("/waypoint/<symbol>/buy-ship/")
@minify_html
@token_required
def buy_ship(symbol, session):
    w = Waypoint(symbol, session)
    if w.shipyard:
        s = Shipyard(symbol, session)
        s.purchase(request.args.get("ship"))
        return jsonify({})
    else:
        abort(404)
