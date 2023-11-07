import textwrap

from autotraders.error import SpaceTradersException
from autotraders.faction import Faction
from autotraders.faction.contract import Contract
from flask import *

from website.paginated_return import paginated_return
from website.session import get_session, anonymous_session
from website.wrappers import token_required, minify_html

faction_bp = Blueprint("faction", __name__)


@faction_bp.route("/factions/")
@minify_html
def factions():
    session = get_session()
    if session is None:
        session = anonymous_session()
    page = int(request.args.get("page", default=1))
    factions = Faction.all(session)
    new_li = paginated_return(factions, page)
    return render_template(
        "faction/factions.html", factions=factions, page=page, li=new_li
    )


@faction_bp.route("/faction/<symbol>/")
@minify_html
def faction(symbol):
    session = get_session()
    if session is None:
        session = anonymous_session()
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
    contracts = Contract.all(session)
    return render_template("faction/contract/contracts.html", contracts=contracts)


@faction_bp.route("/contract/<contract_id>/api/")
@token_required
def contract_api(contract_id, session):
    c = Contract(contract_id, session)
    return render_template("faction/contract/contract_api.html", contract=c)


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
def new_contract(ship, session):
    try:
        c = Contract.negotiate(ship, session)
        return jsonify({})
    except SpaceTradersException as e:
        return jsonify({"error": str(e)})
