import os
from flask import *

from website.bp.faction import faction_bp
from website.bp.main import main_bp
from website.bp.ship import ship_bp
from website.bp.system import system_bp
from website.model import db


def create_app():
    # create the app
    app = Flask(__name__)
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///local.db"
    app.config[
        "SECRET_KEY"
    ] = "secret@!%(@!%!@)*(#$)*$@!)*@!%)*@!)*&%@!132509831207549035213028579674138"
    # initialize the app with the extension
    db.init_app(app)

    app.register_blueprint(ship_bp)
    app.register_blueprint(system_bp)
    app.register_blueprint(faction_bp)
    app.register_blueprint(main_bp)

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    return app
