import pickle
import traceback

import autotraders
import requests
from autotraders.agent import Agent
from autotraders.faction import Faction
from autotraders.map.system import System
from autotraders.session import AutoTradersSession
from flask import *

from website.model import db, User
from website.wrappers import token_required, minify_html

local_bp = Blueprint("local", __name__)


@local_bp.route("/create-user/")
@minify_html
def create_user():
    return render_template("local/create_user.html")


@local_bp.route("/create-user-api/")
def create_user_api():
    db.create_all()
    user = User(token=request.args.get("token").strip(), active=False)
    print(request.args.get("token"))
    db.session.add(user)
    db.session.commit()
    flash("Added User", "success")
    return jsonify({})


@local_bp.route("/select-user/")
@minify_html
def select_user():
    class MockAgent:
        def __init__(self, token, id, active):
            self.token = token
            self.id = id
            self.active = active

    users = []
    for user in db.session.query(User).all():
        try:
            a = Agent(AutoTradersSession(user.token))
            a.active = user.active
            a.id = user.id
            users.append(a)
        except Exception as e:
            users.append(MockAgent(user.token, user.id, user.active))
    return render_template("local/select_user.html", users=users)


@local_bp.route("/select-user-api/<user_id>")
def select_user_api(user_id):
    active_previous = db.session.query(User).filter_by(active=True).first()
    print(active_previous)
    if active_previous is not None:
        active_previous.active = False
    current = db.session.query(User).filter_by(id=user_id).first()
    current.active = True
    db.session.commit()
    return jsonify({})


@local_bp.route("/create-token/")
def create_token():
    return render_template("local/create_token.html")


@local_bp.route("/create-token-api/")
def create_token_api():
    db.create_all()
    t = autotraders.register_agent(
        request.args.get("symbol").strip(),
        request.args.get("faction").strip().upper(),
        request.args.get("email").strip(),
    )
    user = User(token=t)
    db.session.add(user)
    db.session.commit()
    flash("Added User", "success")
    return jsonify({})


@local_bp.route("/delete-user-api/<user_id>")
def delete_user_api(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash("Deleted User", "success")
    return jsonify({})


@local_bp.route("/update-local-data/")
@token_required
def update_local_data(session):
    print("Getting Factions")
    all_factions = Faction.all(session)
    print("Saving Factions")
    sanitized = all_factions[1]
    for faction in sanitized:
        faction.session = None
    pickle.dump(sanitized, open("factions.pickle", "wb"))
    print("Getting Systems")
    try:
        all_systems = []
        data = session.get(session.b_url + "systems.json").json()
        for jsys in data:
            all_systems.append(System(jsys["symbol"], session, jsys))
        sanitized = all_systems
        for system in sanitized:
            system.session = None
            for waypoint in system.waypoints:
                waypoint.session = None
        pickle.dump(all_systems, open("data.pickle", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print("Error getting systems from systems.json, getting from api: " + str(e))
        raise e  # TODO: switch to thread
        all_systems = System.all(session)
        for i in range(1, all_systems.pages + 1):
            all_systems.next()
        print("Writing ...")
        sanitized = all_systems.stitch()
        for system in sanitized:
            system.session = None
            for waypoint in system.waypoints:
                waypoint.session = None

        pickle.dump(sanitized, open("data.pickle", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    return "Success<br><a href=\"/\">Back to the home page</a>"
