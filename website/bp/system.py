from autotraders.waypoint_types.marketplace import Marketplace
from autotraders.waypoint_types.shipyard import Shipyard
from autotraders.system import list_systems, System
from autotraders.waypoint import get_all_waypoints, Waypoint
from flask import *

from website.session import get_session

system_bp = Blueprint('system', __name__)


@system_bp.route('/systems/')
def systems():
    page = int(request.args.get('page', default=1))
    systems_list, total = list_systems(get_session(), page)
    li = {1, 2, 3, 4, 5, 248, 249, 250}
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
    return render_template('systems.html', systems=systems_list,
                           page=page, pages=total, li=new_li)


@system_bp.route('/system/<symbol>/')
def system(symbol):
    return render_template("system.html", system=System(symbol, get_session()),
                           waypoints=get_all_waypoints(symbol, get_session()))


@system_bp.route('/waypoint/<symbol>/')
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
