from autotraders.map.waypoint_types.construction import Construction
from autotraders.map.waypoint_types.jumpgate import JumpGate
from autotraders.map.waypoint_types.marketplace import Marketplace
from autotraders.map.waypoint_types.shipyard import Shipyard
from autotraders.map.system import System
from autotraders.map.waypoint import Waypoint
from flask import *

from website.paginated_return import paginated_return
from website.wrappers import token_required, minify_html

system_bp = Blueprint("system", __name__)


@system_bp.route("/systems/")
@minify_html
@token_required
def systems(session):
    page = int(request.args.get("page", default=1))
    systems_list = System.all(session, page)
    new_li = paginated_return(systems_list, page)
    return render_template("map/systems.html", systems=systems_list, li=new_li)


@system_bp.route("/system/<symbol>/")
@minify_html
@token_required
def system(symbol, session):
    page = int(request.args.get("page", default=1))
    query = str(request.args.get("query", default=""))
    if query.strip() == "":  # TODO: Add support for traits
        query = None
    if query is not None:
        waypoints_list = Waypoint.all(
            session, symbol, waypoint_type=query.upper(), page=page
        )
    else:
        waypoints_list = Waypoint.all(session, symbol, page=page)
    new_li = paginated_return(waypoints_list, page)
    if query is None:
        query = ""
    return render_template(
        "map/system.html",
        system=System(symbol, session),
        waypoints=waypoints_list,
        li=new_li,
        query=query,
    )


@system_bp.route("/system/<symbol>/api-json")
@token_required
def system_api_json(symbol, session):
    system = System(symbol, session)
    json_dict = {
        "symbol": str(system.symbol),
        "type": system.star_type,
        "x": system.x,
        "y": system.y,
        "waypoints": [
            {
                "symbol": str(waypoint.symbol),
                "type": waypoint.waypoint_type,
                "x": waypoint.x,
                "y": waypoint.y,
            }
            for waypoint in system.waypoints
        ],
    }
    return jsonify(json_dict)


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
    if w.waypoint_type == "JUMPGATE":
        j = JumpGate(symbol, session)
    else:
        j = None
    if w.is_under_construction:
        c = Construction(symbol, session)
    else:
        c = None
    return render_template(
        "map/waypoint.html",
        waypoint=w,
        marketplace=m,
        shipyard=s,
        jumpgate=j,
        construction=c,
    )


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
