import autotraders

from website.app import create_app

print(" * Running autotraders version check")
accepted_autotraders_major_version = 1
accepted_autotraders_minor_versions = [8]

autotraders_major_version = int(autotraders.__version__.split(".")[0])
autotraders_minor_version = int(autotraders.__version__.split(".")[1])

if autotraders_major_version > accepted_autotraders_major_version:
    raise ValueError(
        "Please downgrade autotraders to v"
        + str(accepted_autotraders_major_version)
        + "."
        + str(max(accepted_autotraders_minor_versions))
        + ".x"
    )

if (
    autotraders_minor_version not in accepted_autotraders_minor_versions
    and autotraders_minor_version < min(accepted_autotraders_minor_versions)
):
    raise ValueError(
        "Please upgrade autotraders to v"
        + str(accepted_autotraders_major_version)
        + "."
        + str(max(accepted_autotraders_minor_versions))
        + ".x"
    )
elif (
    autotraders_minor_version not in accepted_autotraders_minor_versions
    and autotraders_minor_version < max(accepted_autotraders_minor_versions)
):
    raise ValueError(
        "Please downgrade autotraders to v"
        + str(accepted_autotraders_major_version)
        + "."
        + str(max(accepted_autotraders_minor_versions))
        + ".x"
    )
elif autotraders_minor_version not in accepted_autotraders_minor_versions:
    raise ValueError(
        "Please install autotraders v"
        + str(accepted_autotraders_major_version)
        + "."
        + str(accepted_autotraders_minor_versions)
        + ".x"
    )
print(" * Acceptable version found: Autotraders v" + autotraders.__version__)

if __name__ == "__main__":
    create_app().run(debug=True)
