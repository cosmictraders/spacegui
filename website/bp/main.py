from autotraders.agent import Agent
from flask import *

from website.session import get_session

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    s = get_session()
    agent = Agent(s)
    return render_template("index.html", agent=agent)


@main_bp.route("/map/")
def map():
    return render_template("map.html")


@main_bp.route("/map/tile/{z}/{x}/{y}.png")
def map_api(z, x, y):
    abort(404)
