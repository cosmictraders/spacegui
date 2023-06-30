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
    factions = Faction.all(session)[1]
    for faction in factions:
        faction.description = textwrap.shorten(
            faction.description, width=250, placeholder=" ..."
        )
    return render_template("faction/factions.html", factions=factions)


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
def contract_api(contract_id, session):
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
