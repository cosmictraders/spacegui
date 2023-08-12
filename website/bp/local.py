import autotraders
import requests
from autotraders.agent import Agent
from autotraders.session import get_session
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
            a = Agent(get_session(user.token))
            a.active = user.active
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
