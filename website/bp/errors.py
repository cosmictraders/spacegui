from autotraders import SpaceTradersException
from flask import Blueprint, render_template, Response, redirect, flash, url_for

errors_bp = Blueprint("error", __name__)


@errors_bp.app_errorhandler(404)
def not_found(e):
    resp = Response(render_template("error/not_found.html"))
    resp.status_code = 404
    return resp


@errors_bp.app_errorhandler(500)
def error_500(e):
    original_exception = e.original_exception
    if isinstance(original_exception, SpaceTradersException):  # TODO: Not for every issue though
        flash(str(original_exception), "danger")
        return redirect(url_for("local.select_token"))
    resp = Response(render_template("error/500.html"))
    resp.status_code = 500
    return resp
