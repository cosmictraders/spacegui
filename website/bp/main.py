import autotraders
import requests
from autotraders.agent import Agent
from flask import *

from website.model import db, User
from website.wrappers import token_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
@token_required
def index(session):
    agent = Agent(session)
    return render_template("index.html", agent=agent)


@main_bp.route("/setup/")
def setup():
    return render_template("setup.html")


@main_bp.route("/create-token/")
def create_token():
    return render_template("create_token.html")


@main_bp.route("/create-token-api/")
def create_token():
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
def create_user():
    db.drop_all()
    db.create_all()
    user = User(token=request.args.get("token").strip())
    db.session.add(user)
    db.session.commit()
    flash("Added User", "success")
    return jsonify({})


@main_bp.route("/map/")
def map_v3():
    return render_template("map.html")


@main_bp.route("/info/")
def info():
    status = autotraders.get_status()
    users = db.session.execute(db.select(User)).first()
    if users is not None:
        t = users[0].token
    else:
        t = "No Token"
    return render_template("info.html", status=status, token=t)


@main_bp.route("/settings/")
def settings():
    users = db.session.execute(db.select(User)).first()
    if users is not None:
        t = users[0].token
    else:
        t = ""
    return render_template("settings.html", token=t)


@main_bp.route("/settings-api/")
def settings_api():
    users = db.session.execute(db.select(User)).first()
    pass
