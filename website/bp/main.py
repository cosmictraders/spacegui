import difflib
import pickle
from datetime import datetime, timezone

import autotraders
import requests
from autotraders.agent import Agent
from autotraders.ship import Ship
from flask import *

from website.model import db, User
from website.wrappers import token_required, minify_html

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
@minify_html
@token_required
def index(session):
    agent = Agent(session)
    return render_template("index.html", agent=agent)


@main_bp.route("/setup/")
@minify_html
def setup():
    return render_template("setup.html")


@main_bp.route("/create-token/")
@minify_html
def create_token():
    return render_template("create_token.html")


@main_bp.route("/create-token-api/")
@minify_html
def create_token_api():
    db.drop_all()
    db.create_all()
    r = requests.post(
        "https://api.spacetraders.io/v2/register",
        data={
            "faction": request.args.get("faction").strip().upper(),
            "symbol": request.args.get("symbol").strip(),
            "email": request.args.get("email").strip(),
        },
    )
    user = User(token=r.json()["data"]["token"])
    db.session.add(user)
    db.session.commit()
    flash("Added User", "success")
    return jsonify({})


@main_bp.route("/reset/")
def reset():
    db.drop_all()
    flash("Reset successful", "primary")
    return redirect("/")


@main_bp.route("/create-user/")
@minify_html
def create_user():
    db.drop_all()
    db.create_all()
    user = User(token=request.args.get("token").strip())
    db.session.add(user)
    db.session.commit()
    flash("Added User", "success")
    return jsonify({})


@main_bp.route("/map/")
@minify_html
def map_v3():
    return render_template("map/map.html")


def rich_format(s):
    if "https://" in s:
        splt = s.split("https://")
        new_s = f'{splt[0]}<a target=\"_blank\" href=\"https://{splt[1]}\">https://{splt[1]}</a>'
        return new_s
    return s


@main_bp.route("/settings/")
@minify_html
def settings():
    users = db.session.execute(db.select(User)).first()
    status = autotraders.get_status()
    server_announcements = status.announcements
    announcements = []
    for server_announcement in server_announcements:
        announcements.append(server_announcement.title + " - " + rich_format(server_announcement.body))
    if users is not None:
        t = users[0].token
    else:
        t = ""
    return render_template("settings.html", announcements=announcements, status=status, token=t,
                           tz=datetime.now(timezone.utc).astimezone().tzinfo)


@main_bp.route("/settings-api/")
def settings_api():
    users = db.session.execute(db.select(User)).first()
    t = users[0].token
    updated = []
    input_token = request.args.get("token", t).strip(" ").strip("\"").strip("\'")
    if input_token not in [t, "", " "]:
        if len(input_token) < 5:
            return jsonify({"error": "Token too short"})
        else:
            users[0].token = request.args.get("token", t)
            db.session.commit()
            updated.append("token")
    return jsonify({"updated": updated})


@main_bp.route("/automations/")
def automations():
    return render_template("automations.html")


@main_bp.route("/automation/<name>/")
def automation(name):
    return render_template("automation.html", name=name)


def weight(query, s):
    weight = difflib.SequenceMatcher(None, query, s).ratio()
    return weight * 2 - 1


@main_bp.route("/search/")
@token_required
def search(session):
    query = request.args.get("query")
    system_data = pickle.load(open("./data.pickle", "rb"))
    unweighted_map = []
    for item in system_data:
        if weight(query, str(item.symbol)) > 0:
            unweighted_map.append((item, weight(query, str(item.symbol))))
            for waypoint in item.waypoints:
                if weight(query, str(waypoint.symbol)) != 0:
                    unweighted_map.append((waypoint, weight(query, str(waypoint.symbol))))
    smap = sorted(unweighted_map, key=lambda x: x[1], reverse=True)
    amap = []
    for item, _ in smap:
        amap.append(item)
    if len(amap) > 105:
        amap = amap[:100]
    ship_data = Ship.all(session)[1]
    if "ship" in query:
        ships = ship_data
    else:
        ships = []
        for item in ship_data:
            if weight(query, item.symbol) > 0:
                ships.append(item)
    return render_template("search.html", query=query, map=amap, ships=ships)
