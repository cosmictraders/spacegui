import textwrap

from autotraders.faction import Faction
from autotraders.faction.contract import Contract
from flask import *

from website.wrappers import token_required, minify_html

faction_bp = Blueprint("faction", __name__)


@faction_bp.route("/factions/")
@minify_html
@token_required
def factions(session):
    page = int(request.args.get("page", default=1))
    factions = Faction.all(session)
    li = {
        1
    }
    if factions.pages > 1:
        li.add(2)
        if factions.pages > 2:
            li.add(3)
            if factions.pages > 3:
                li.add(4)
                if factions.pages > 4:
                    li.add(5)
    if factions.pages > 0:
        li.add(factions.pages - 2)
    if factions.pages > 0:
        li.add(factions.pages - 1)
    if factions.pages > 0:
        li.add(factions.pages)
    li = list(li)
    li.sort()
    new_li = []
    prev = 0
    for i in li:
        if i != (prev + 1):
            new_li.append("..")
        new_li.append(i)
        prev = i
    return render_template("faction/factions.html", factions=factions, page=page, li=new_li)


@faction_bp.route("/faction/<symbol>/")
@minify_html
@token_required
def faction(symbol, session):
    light_background = {}.get(symbol, "")
    dark_background = {}.get(symbol, "")
    force_dark = {"VOID": True}.get(symbol, False)
    return render_template(
        "faction/faction.html",
        faction=Faction(symbol, session),
        light_background=light_background,
        dark_background=dark_background,
        force_dark=force_dark,
    )


@faction_bp.route("/contracts/")
@minify_html
@token_required
def contracts(session):
    c = Contract.all(session)
    return render_template("faction/contract/contracts.html", contracts=c)


@faction_bp.route("/contract/<contract_id>/api/")
@token_required
def contract_api(contract_id, session):  # TODO: port to html
    contract = Contract(contract_id, session)
    return jsonify(
        {
            "deadline": str(
                contract.deadline.astimezone(tz=None).strftime("%Y-%m-%d %I:%M:%S")
            ),
            "accepted": contract.accepted,
            "fulfilled": contract.fulfilled,
        }
    )


@faction_bp.route("/contract/<contract_id>/")
@minify_html
@token_required
def contract(contract_id, session):
    c = Contract(contract_id, session)
    return render_template("faction/contract/contract.html", contract=c)


@faction_bp.route("/contract/<contract_id>/accept")
@token_required
def accept_contract(contract_id: str, session):
    try:
        c = Contract(contract_id, session)
        c.accept()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": str(e)})


@faction_bp.route("/contract/<contract_id>/fulfill")
@token_required
def fulfill_contract(contract_id: str, session):
    try:
        c = Contract(contract_id, session)
        c.fulfill()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": str(e)})


@faction_bp.route("/contract/new/<ship>/")
@token_required
def sandbox(ship, session):
    try:
        c = Contract.negotiate(ship, session)
        return jsonify({})
    except IOError as e:
        return jsonify({"error": str(e)})
