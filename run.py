import autotraders
import click

from website.app import create_app
from website.config import BaseConfig

print(f" * Running autotraders version check for version v{autotraders.__version__}")
accepted_autotraders_major_version = 2
accepted_autotraders_minor_versions = [2, 3]
warning_autotraders_minor_versions = [2]
blacklisted_versions = ["2.2.0", "2.2.1", "2.2.3", "2.2.4"]

autotraders_major_version = int(autotraders.__version__.split(".")[0])
autotraders_minor_version = int(autotraders.__version__.split(".")[1])

if autotraders.__version__ in blacklisted_versions:
    raise ValueError(
        f"Please upgrade autotraders to v{accepted_autotraders_major_version}.{max(accepted_autotraders_minor_versions)}, your version has been blacklisted, which means it is likely no longer supported by the server.")

if autotraders_major_version > accepted_autotraders_major_version:
    raise ValueError(
        f"Please downgrade autotraders to v{accepted_autotraders_major_version}.{max(accepted_autotraders_minor_versions)}")

if (
        autotraders_minor_version not in accepted_autotraders_minor_versions
        and autotraders_minor_version < min(accepted_autotraders_minor_versions)
):
    raise ValueError(
        f"Please upgrade autotraders to v{accepted_autotraders_major_version}.{max(accepted_autotraders_minor_versions)}")
elif (
        autotraders_minor_version not in accepted_autotraders_minor_versions
        and autotraders_minor_version < max(accepted_autotraders_minor_versions)
):
    raise ValueError(
        f"Please downgrade autotraders to v{accepted_autotraders_major_version}.{max(accepted_autotraders_minor_versions)}")
elif autotraders_minor_version not in accepted_autotraders_minor_versions:
    raise ValueError(
        f"Please install autotraders v{accepted_autotraders_major_version}.{max(accepted_autotraders_minor_versions)}")
elif autotraders_minor_version in warning_autotraders_minor_versions:
    print(
        f" * Warning: Autotraders v{autotraders.__version__} is not officially supported, but limited functionality might be available, proceed at your own risk.")


@click.command()
@click.option("--debug", is_flag=True)
@click.option("--port", default=5000)
@click.option("--threaded", is_flag=True)
@click.option("--db", default="sqlite:///local.db")
@click.option("--secret-key", default="secret@!%(@!%!@)*(#$)*$@!)*@!%)*@!)*&%@!132509831207549035213028579674138")
def cmd(debug, port, threaded, db, secret_key):
    BaseConfig.SECRET_KEY = secret_key
    BaseConfig.SQLALCHEMY_DATABASE_URI = db
    create_app().run(debug=debug, port=port, threaded=threaded)


if __name__ == "__main__":
    cmd()
