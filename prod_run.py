import click

from website.app import create_app
from website.config import BaseConfig


@click.command()
@click.option("--db", default="sqlite:///local.db")
@click.option("--secret-key", default="secret@!%(@!%!@)*(#$)*$@!)*@!%)*@!)*&%@!132509831207549035213028579674138")
def cmd(db, secret_key):
    BaseConfig.SECRET_KEY = secret_key
    BaseConfig.SQLALCHEMY_DATABASE_URI = db
    create_app().run(debug=False, host="0.0.0.0", port=8000, threaded=False)


if __name__ == "__main__":
    cmd()
