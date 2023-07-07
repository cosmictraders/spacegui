import inspect
import pickle
import time
from datetime import datetime, timezone

import autotraders
import requests
from autotraders.agent import Agent
from autotraders.faction.contract import Contract
from autotraders.ship import Ship
from flask import *

from website.model import db, User, Automation
from website.search import (
    weight,
    read_query,
    check_filters_system,
    check_filters_waypoint,
    check_filters_ship,
    check_filters_contract,
    check_filters_faction,
)
from website.wrappers import token_required, minify_html

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
@minify_html
@token_required
def index(session):
    agent = Agent(session)
    return render_template("index.html", agent=agent)


@main_bp.route("/map/")
@minify_html
def map_v3():
    return render_template("map/map.html")


@main_bp.route("/map-v4/")
@minify_html
def map_v4():
    return render_template("map/map_v4.html")


def rich_format(s):
    if "https://" in s:
        splt = s.split("https://")
        new_s = f'{splt[0]}<a target="_blank" href="https://{splt[1]}">https://{splt[1]}</a>'
        return new_s
    return s


@main_bp.route("/settings/")
@minify_html
def settings():
    db.create_all()
    users = db.session.execute(db.select(User)).first()
    status = autotraders.get_status()
    server_announcements = status.announcements
    announcements = []
    for server_announcement in server_announcements:
        announcements.append(
            server_announcement.title + " - " + rich_format(server_announcement.body)
        )
    if users is not None:
        t = users[0].token
    else:
        t = ""
    return render_template(
        "settings.html",
        announcements=announcements,
        status=status,
        token=t,
        tz=datetime.now(timezone.utc).astimezone().tzinfo,
    )


@main_bp.route("/settings-api/")
def settings_api():
    users = db.session.execute(db.select(User)).first()
    if users is None:
        # TODO: Fix
        pass
    t = users[0].token
    updated = []
    input_token = request.args.get("token", t).strip(" ").strip('"').strip("'")
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
    return render_template("automations.html", automations=Automation.all())


@main_bp.route("/automation/<name>/")
def automation(name):
    return render_template("automation.html", name=name)


@main_bp.route("/search/")
@token_required
def search(session):
    page = int(request.args.get("page", default=1))
    t1 = (
        time.time()
    )  # TODO: Speed improvements by only querying whats needed (`is: waypoint` should not be getting ship,contract info)
    query, filters = read_query(request.args.get("query"))
    system_data = pickle.load(open("./data.pickle", "rb"))
    t1_2 = time.time()
    faction_data = pickle.load(open("./factions.pickle", "rb"))
    t1_3 = time.time()
    unweighted_map = []
    ship_data = Ship.all(session)[1]
    contract_data = Contract.all(session)[1]
    t1_4 = time.time()
    for item in system_data:
        if weight(query, str(item.symbol)) > -0.1:
            if check_filters_system(item, filters):
                unweighted_map.append((item, weight(query, str(item.symbol))))
        if weight(query, str(item.symbol)) > -0.2:
            for waypoint in item.waypoints:
                if weight(query, str(waypoint.symbol)) > 0 and check_filters_waypoint(
                        waypoint, filters
                ):
                    unweighted_map.append(
                        (waypoint, weight(query, str(waypoint.symbol)))
                    )
    t1_5 = time.time()
    for item in faction_data:
        if (
                weight(query, item.symbol) > -0.25 or weight(query, item.name) > -0.25
        ) and check_filters_faction(item, filters):
            unweighted_map.append((item, weight(query, str(item.symbol))))
    t1_6 = time.time()
    for item in ship_data:
        if weight(query, item.symbol) > -0.25 and check_filters_ship(item, filters):
            unweighted_map.append((item, weight(query, item.symbol)))
    for item in contract_data:
        if weight(query, item.contract_id) > -0.7 and check_filters_contract(item, filters):
            unweighted_map.append((item, weight(query, str(item.contract_id))))
    amap = [
        item for item, _ in sorted(unweighted_map, key=lambda x: x[1], reverse=True)
    ]
    t2 = time.time()
    print(t1_2 - t1, t1_3 - t1_2, t1_4 - t1_3, t1_5 - t1_4, t1_6 - t1_5, t2 - t1_6)
    li = {
        1
    }
    if len(amap) // 100 > 1:
        li.add(2)
        if len(amap) // 100 > 2:
            li.add(3)
            if len(amap) // 100 > 3:
                li.add(4)
                if len(amap) // 100 > 4:
                    li.add(5)
    if len(amap) // 100 - 2 > 0:
        li.add(len(amap) // 100 -2)
    if len(amap) // 100 - 1 > 0:
        li.add(len(amap) // 100 -1)
    if len(amap) // 100 > 0:
        li.add(len(amap) // 100)
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
        "search.html", query=request.args.get("query"), map=amap[(page - 1) * 100: page * 100], time=str(t2 - t1), li=new_li, page=page,
        pages=len(amap) // 100
    )
