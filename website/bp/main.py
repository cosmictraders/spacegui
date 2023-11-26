from datetime import datetime, timezone

import autotraders
from autotraders.agent import Agent
from autotraders.faction.contract import Contract
from autotraders.ship import Ship
from flask import *

from website.model import db, User, Automation, Token
from website.session import get_session, anonymous_session, get_user
from website.wrappers import token_required, minify_html

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
@minify_html
def index():
    session = get_session()
    if session is None:
        return render_template("landing.html")
    agent = Agent(session)
    return render_template(
        "index.html",
        agent=agent,
        ships=Ship.all(session),
        contracts=Contract.all(session),
    )


def rich_format(s):
    if "https://" in s:
        splt = s.split("https://")
        new_s = f'{splt[0]}<a target="_blank" href="https://{splt[1]}">https://{splt[1]}</a>'
        return new_s
    return s


@main_bp.route("/settings/")
@minify_html
def settings():
    db.create_all()
    user = get_user()
    token = None
    if user is not None:
        token = db.session.query(Token).filter_by(user=user.id).first()  # TODO: Filter by user id
    status = autotraders.get_status()
    server_announcements = status.announcements
    announcements = []
    for server_announcement in server_announcements:
        announcements.append(
            server_announcement.title + " - " + rich_format(server_announcement.body)
        )
    if token is not None:
        t = token.token
    else:
        t = ""
    return render_template(
        "settings.html",
        announcements=announcements,
        status=status,
        token=t,
        tz=datetime.now(timezone.utc).astimezone().tzinfo,
    )


@main_bp.route("/settings-api/")
def settings_api():  # TODO: This is a security risk, need to filter tokens instead (make sure to filter by current user id)
    pass
    # users = db.session.query(User).filter_by(active=True).first()
    # if users is None:
    #     resp = jsonify({"error": "No active user found."})
    #     return resp
    # t = users[0].token
    # updated = []
    # input_token = request.args.get("token", t).strip(" ").strip('"').strip("'")
    # if input_token not in [t, "", " "]:
    #     if len(input_token) < 5:
    #         return jsonify({"error": "Token too short"})
    #     else:
    #         users[0].token = request.args.get("token", t)
    #         db.session.commit()
    #         updated.append("token")
    # return jsonify({"updated": updated})


@main_bp.route("/automations/")
def automations():
    return render_template(
        "automation/automations.html", automations=db.session.query(Automation).all()
    )


@main_bp.route("/new-automation/")
def new_automation():
    return render_template("automation/new_automation.html")


@main_bp.route("/automation/<i>/")
def automation(i):
    return render_template(
        "automation/automation.html",
        automation=db.session.query(Automation).filter_by(id=i).first(),
    )


@main_bp.route("/agents/")
@minify_html
def agents():
    session = get_session()
    if session is None:
        session = anonymous_session()
    page = int(request.args.get("page", default=1))
    agents_list = Agent.all(session, page)
    li = {1}
    if agents_list.pages > 1:
        li.add(2)
        if agents_list.pages > 2:
            li.add(3)
            if agents_list.pages > 3:
                li.add(4)
                if agents_list.pages > 4:
                    li.add(5)
    if agents_list.pages > 0:
        li.add(agents_list.pages - 2)
    if agents_list.pages > 0:
        li.add(agents_list.pages - 1)
    if agents_list.pages > 0:
        li.add(agents_list.pages)
    li.add(page)
    if page > min(li):
        li.add(page - 1)
    if page < max(li):
        li.add(page + 1)
    li = list(li)
    li.sort()
    new_li = []
    prev = 0
    for i in li:
        if i != (prev + 1):
            new_li.append("..")
        new_li.append(i)
        prev = i
    return render_template("agent/agents.html", agents=agents_list, li=new_li)


@main_bp.route("/agent/<symbol>/")
@minify_html
def agent(symbol):
    session = get_session()
    if session is None:
        session = anonymous_session()
    return render_template("agent/agent.html", agent=Agent(session, symbol))


@main_bp.route("/leaderboard/")
def leaderboard():
    return render_template("leaderboard.html", status=autotraders.get_status())


@main_bp.route("/create-all/")
def create_all():
    db.create_all()
    return "Created all tables"
