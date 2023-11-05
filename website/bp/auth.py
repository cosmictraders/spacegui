from flask import Blueprint, redirect, render_template

from website.session import logout_session
from website.wrappers import login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register")
def register():
    return render_template("auth/register.html")


@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout(user):
    logout_session()
    return redirect("/")
