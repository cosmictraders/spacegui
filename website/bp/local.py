import requests
from flask import *

from website.model import db, User
from website.wrappers import token_required, minify_html

local_bp = Blueprint("local", __name__)


@local_bp.route("/create-user/")
@minify_html
def create_user():
    return render_template("local/create_user.html")


@local_bp.route("/create-user-api/")
@minify_html
def create_user_api():
    db.create_all()
    user = User(token=request.args.get("token").strip(), active=False)
    db.session.add(user)
    db.session.commit()
    flash("Added User", "success")
    return jsonify({})


@local_bp.route("/select-user/")
@minify_html
def select_user():
    return render_template("local/select_user.html", users=db.session.query(User).all())


@local_bp.route("/select-user-api/<user_id>")
def select_user_api(user_id):
    active_previous = db.session.query(User).filter_by(active=True).first()
    if active_previous is not None:
        active_previous.active = False
    current = db.session.query(User).filter_by(id=user_id).first()
    current.active = True
    db.session.commit()
    return jsonify({})


@local_bp.route("/select-user-api/<user_id>")
def delete_user_api(user_id):
    current = db.session.query(User).filter_by(id=user_id).first()
    db.session.delete(current)
    db.session.commit()
    return jsonify({})


@local_bp.route("/create-token/")
def create_token():
    return render_template("local/create_token.html")


@local_bp.route("/create-token-api/")
def create_token_api():
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
