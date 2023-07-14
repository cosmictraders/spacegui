import autotraders

from website.app import create_app

assert autotraders.__version__.split(".")[0] == "1"
assert autotraders.__version__.split(".")[1] == "7"

if __name__ == "__main__":
    create_app().run(debug=True)
