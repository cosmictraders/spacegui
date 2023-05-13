import time

from autotraders.agent import Agent
from flask import *

from website.session import get_session

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    s = get_session()
    agent = Agent(s)
    return render_template('index.html', agent=agent)


@main_bp.route('/map/')
def map():
    s = get_session()
    r = s.get("https://api.spacetraders.io/v2/systems?limit=20")
    r2 = s.get("https://api.spacetraders.io/v2/systems?limit=20&page=2")
    time.sleep(2)
    r3 = s.get("https://api.spacetraders.io/v2/systems?limit=20&page=3")
    time.sleep(2)
    r4 = s.get("https://api.spacetraders.io/v2/systems?limit=20&page=3")
    j = r.json()
    j1 = r2.json()
    j2 = r3.json()
    j3 = r4.json()
    systems = []
    for system_json in j["data"]:
        systems.append("[" + str(system_json["x"]) + "," + str(system_json["y"]) + "]")
    for system_json in j1["data"]:
        systems.append("[" + str(system_json["x"]) + "," + str(system_json["y"]) + "]")
    for system_json in j2["data"]:
        systems.append("[" + str(system_json["x"]) + "," + str(system_json["y"]) + "]")
    for system_json in j3["data"]:
        systems.append("[" + str(system_json["x"]) + "," + str(system_json["y"]) + "]")
    return render_template('map.html', coords="[" + ",".join(systems) + "]")
