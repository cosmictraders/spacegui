import os
from flask import *

from website.bp.auth import auth_bp
from website.bp.errors import errors_bp
from website.bp.faction import faction_bp
from website.bp.local import local_bp
from website.bp.main import main_bp
from website.bp.map import map_bp
from website.bp.search import search_bp
from website.bp.ship import ship_bp
from website.bp.system import system_bp
from website.config import BaseConfig
from website.model import db
from website.session import get_user


def create_app():
    # create the app
    app = Flask(__name__)
    # configure the SQLite database, relative to the app instance folder
    app.config.from_object(BaseConfig)
    # initialize the app with the extension
    db.init_app(app)
    app.register_blueprint(ship_bp)
    app.register_blueprint(system_bp)
    app.register_blueprint(faction_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(local_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    class UserTemplate:
        def __init__(self, auth):
            self.is_authenticated = auth

    @app.context_processor
    def inject_user():
        user = get_user()
        if user is not None:
            user = UserTemplate(True)
        else:
            user = UserTemplate(False)
        return dict(user=user)

    return app
