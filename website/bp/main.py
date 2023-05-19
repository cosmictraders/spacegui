import os
from io import BytesIO
from pathlib import Path

import sqlalchemy
from PIL import Image
from autotraders.agent import Agent
from flask import *

from website.model import db, User
from website.session import get_session

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index():
    try:
        s = get_session()
    except Exception as e:
        print(e)
        db.create_all()
        return render_template("setup.html")
    agent = Agent(s)
    return render_template("index.html", agent=agent)

@main_bp.route("/reset/")
def reset():
    db.drop_all()
    return "Done!"


@main_bp.route("/create-user/")
def create_user():
    db.drop_all()
    db.create_all()
    user = User(token=request.args.get("token").strip())
    db.session.add(user)
    db.session.commit()
    print("added")
    return jsonify({})

@main_bp.route("/map-v3/")
def map_v3():
    return render_template("map_v3.html")
