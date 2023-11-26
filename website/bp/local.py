import pickle
from typing import Any

import autotraders
from autotraders.agent import Agent
from autotraders.faction import Faction
from autotraders.faction.contract import Contract
from autotraders.map.system import System
from autotraders.session import AutoTradersSession
from autotraders.ship import Ship
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
import json
from website.model import db, User, Token
from website.wrappers import token_required, minify_html, login_required

local_bp = Blueprint("local", __name__)


@local_bp.route("/add-token/")
@minify_html
@login_required
def add_token(user):
    return render_template("local/add_token.html")


@local_bp.route("/add-existing-token/")
@minify_html
@login_required
def add_existing_token(user):
    return render_template("local/add_existing_token.html")


@local_bp.route("/add-existing-token-api/")
@login_required
def add_existing_token_api(user):
    db.create_all()
    user = User(token=request.args.get("token").strip(), active=False, user=user.id)
    db.session.add(user)
    db.session.commit()
    flash("Added User", "success")
    return jsonify({})


@local_bp.route("/select-token/")
@minify_html
@login_required
def select_token(user):
    if db.session.query(Token).filter_by(user=user.id).count() == 0:
        flash("No tokens found, please create one", "info")
        return redirect(url_for("local.add_token"))

    class MockAgent:
        def __init__(self, token, id, active):
            self.token = token
            self.id = id
            self.active = active

    tokens = []
    for token in db.session.query(Token).filter_by(user=user.id).all():
        try:
            a = Agent(AutoTradersSession(token.token))
            a.active = token.active
            a.id = token.id
            a.token = token.token
            tokens.append(a)
        except Exception as e:
            tokens.append(MockAgent(token.token, token.id, token.active))
    return render_template("local/select_token.html", tokens=tokens)


@local_bp.route("/select-user-api/<token_id>")
@login_required
def select_user_api(token_id, user):
    active_previous = (
        db.session.query(Token).filter_by(active=True, user=user.id).first()
    )
    if active_previous is not None:
        active_previous.active = False
    current = db.session.query(Token).filter_by(id=token_id, user=user.id).first()
    current.active = True
    db.session.commit()
    return jsonify({})


@local_bp.route("/create-token/")
@minify_html
@login_required
def create_user_no_token(user):
    return render_template("local/create_token.html")


@local_bp.route("/create-token-api/")
@login_required
def create_user_no_token_api(user):
    db.create_all()
    t = autotraders.register_agent(
        request.args.get("symbol").strip(),
        request.args.get("faction").strip().upper(),
        request.args.get("email").strip(),
    )
    token = Token(token=t, user=user.id)  # TODO: Fix
    db.session.add(token)
    db.session.commit()
    flash("Added User", "success")
    return jsonify({})


@local_bp.route("/delete-token-api/<token_id>")
@login_required
def delete_user_api(token_id, user):
    token = Token.query.filter_by(id=token_id).first()
    if token.user != user.id:
        flash("You do not own this token", "danger")
        return jsonify({})
    db.session.delete(token)
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
        data: list[dict[str, Any]] = session.get(
            str(session.base_url) + "systems.json"
        ).json()
        for jsys in data:
            all_systems.append(System(jsys["symbol"], session, jsys))
        sanitized = all_systems
        for system in sanitized:
            system.session = None
            for waypoint in system.waypoints:
                waypoint.session = None
        pickle.dump(
            all_systems, open("data.pickle", "wb"), protocol=pickle.HIGHEST_PROTOCOL
        )
    except Exception as e:
        print("Error getting systems from systems.json, getting from api: " + str(e))
        all_systems = System.all(session)
        for i in range(1, all_systems.pages + 1):
            all_systems.next()
        print("Writing ...")
        sanitized = all_systems.stitch()
        for system in sanitized:
            system.session = None
            for waypoint in system.waypoints:
                waypoint.session = None

        pickle.dump(
            sanitized, open("data.pickle", "wb"), protocol=pickle.HIGHEST_PROTOCOL
        )

    data: list[System] = sanitized
    data_dict = {}
    for i in data:
        waypoints = {}
        for w in i.waypoints:
            traits = []
            if w.traits is not None:
                for trait in w.traits:
                    traits.append(trait.symbol)
            waypoints[str(w.symbol)] = {
                "x": w.x,
                "y": w.y,
                "traits": traits,
                "type": w.waypoint_type,
            }
        data_dict[str(i.symbol)] = {
            "type": i.star_type,
            "x": i.x,
            "y": i.y,
            "factions": i.factions,
            "waypoints": waypoints,
            "num_waypoints": len(waypoints),
        }
    json.dump(data_dict, open("./website/static/systems.json", "w"), indent=4)
    return 'Success<br><a href="/">Back to the home page</a>'
