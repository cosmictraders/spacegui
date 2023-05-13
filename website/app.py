from flask import *

from website.bp.contract import contract_bp
from website.bp.main import main_bp
from website.bp.ship import ship_bp
from website.bp.system import system_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(ship_bp)
    app.register_blueprint(system_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(main_bp)
    return app