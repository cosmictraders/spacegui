from autotraders import SpaceTradersException
from autotraders.map.system import System
from flask import Blueprint, render_template, Response, redirect, flash, url_for, jsonify

from website.wrappers import minify_html, token_required

map_bp = Blueprint("map", __name__)


@map_bp.route("/map/")
@minify_html
def map_v3():
    return render_template("map/map.html")


@map_bp.route("/map-v4/")
@minify_html
def map_v4():
    return render_template("map/map_v4.html")


@map_bp.route("/system-map/<system>")
@token_required
@minify_html
def system_map(system, session):
    return render_template("map/system_map.html", system=system)


@map_bp.route("/system-map-api/<system>")
@token_required
def system_map_api(system, session):
    system_data = System(system, session)
    j = {
        "symbol": str(system_data.symbol),
        "x": system_data.x,
        "y": system_data.y,
        "type": system_data.star_type,
        "waypoints": [{"symbol": str(w.symbol), "x": w.x, "y": w.y, "type": w.waypoint_type} for w in system_data.waypoints]
    }
    return jsonify(j)
