import json

import werkzeug.security
from flask import Blueprint, redirect, render_template, request, abort, jsonify

from website.model import db, User
from website.session import logout_session, login_session
from website.wrappers import login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register")
def register():
    return render_template("auth/register.html")


@auth_bp.route("/register-api")
def register_api():
    if request.method == "POST":
        data_json = json.loads(request.data)
        username = data_json["username"]
        password = data_json["password"]
        requested_user = db.session.query(User).filter_by(username=username).first()
        if requested_user is None:
            user = User(username=username, password=werkzeug.security.generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            login_session(user)
            return jsonify({"success": True})
        else:
            abort(401)
    else:
        abort(405)


@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")


@auth_bp.route("/login-api")
def login_api():
    if request.method == "POST":
        data_json = json.loads(request.data)
        username = data_json["username"]
        password = data_json["password"]
        requested_user = db.session.query(User).filter_by(username=username).first()
        if requested_user is None:
            abort(404)
        else:
            if werkzeug.security.check_password_hash(requested_user.password, password):
                login_session(requested_user)
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})
    else:
        abort(405)


@auth_bp.route("/logout")
@login_required
def logout(user):
    logout_session()
    return redirect("/")
