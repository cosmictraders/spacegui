from autotraders.faction.contract import Contract, get_all_contracts
from flask import *

from website.session import get_session

contract_bp = Blueprint("contract", __name__)


@contract_bp.route("/contracts/")
def contracts():
    s = get_session()
    return render_template("contracts.html", contracts=get_all_contracts(s))


@contract_bp.route("/contract/<contract_id>/api/")
def contract_api(contract_id):
    s = get_session()
    contract = Contract(contract_id, s)
    return jsonify(
        {
            "deadline": str(contract.deadline),
            "accepted": contract.accepted,
            "fulfilled": contract.fulfilled,
        }
    )


@contract_bp.route("/contract/<contract_id>/")
def contract(contract_id):
    s = get_session()
    c = Contract(contract_id, s)
    return render_template("contract.html", contract=c)


@contract_bp.route("/contract/<contract_id>/accept")
def accept_contract(contract_id: str):
    try:
        s = get_session()
        c = Contract(contract_id, s)
        c.accept()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": str(e)})


@contract_bp.route("/contract/<contract_id>/fulfill")
def fulfill_contract(contract_id: str):
    try:
        s = get_session()
        c = Contract(contract_id, s)
        c.fulfill()
        return jsonify({})
    except IOError as e:
        return jsonify({"error": str(e)})
