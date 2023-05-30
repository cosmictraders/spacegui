from autotraders.faction.contract import Contract, get_all_contracts
from flask import *

from website.wrappers import token_required, minify_html

contract_bp = Blueprint("contract", __name__)


@contract_bp.route("/contracts/")
@minify_html
@token_required
def contracts(session):
    return render_template("contracts.html", contracts=get_all_contracts(session))


@contract_bp.route("/contract/<contract_id>/api/")
def contract_api(contract_id, session):
    contract = Contract(contract_id, session)
    return jsonify(
        {
            "deadline": str(contract.deadline),
            "accepted": contract.accepted,
            "fulfilled": contract.fulfilled,
        }
    )


@contract_bp.route("/contract/<contract_id>/")
@minify_html
@token_required
def contract(contract_id, session):
    c = Contract(contract_id, session)
    return render_template("contract.html", contract=c)


@contract_bp.route("/contract/<contract_id>/accept")
def accept_contract(contract_id: str, session):
    try:
        c = Contract(contract_id, session)
        c.accept()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": str(e)})


@contract_bp.route("/contract/<contract_id>/fulfill")
def fulfill_contract(contract_id: str, session):
    try:
        c = Contract(contract_id, session)
        c.fulfill()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": str(e)})
