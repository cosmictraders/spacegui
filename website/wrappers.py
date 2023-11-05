import autotraders.token
from flask import redirect, url_for, flash, session
from minify_html import minify

from website.session import get_session, get_user


def minify_html(func):
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        if type(result) is str:
            return minify(
                result,
                do_not_minify_doctype=True,
                ensure_spec_compliant_unquoted_attribute_values=True,
                keep_closing_tags=True,
                keep_comments=False,
                keep_html_and_head_opening_tags=True,
                keep_spaces_between_attributes=True,
                minify_css=True,
                minify_js=False,
                remove_bangs=False,
                remove_processing_instructions=False,
            )
        else:
            print("WARNING: Minifying failed because result was not string")
            return result

    wrap.__name__ = func.__name__
    wrap.__doc__ = func.__doc__
    return wrap


def token_required(func):
    def wrap(*args, **kwargs):
        try:
            session = get_session()
        except Exception as e:
            if type(e) == AttributeError:
                flash("No active token found", "danger")
            else:
                flash(str(type(e)) + " - " + str(e), "danger")
            return redirect(url_for("local.select_user"))
        result = func(*args, **kwargs, session=session)
        return result

    wrap.__name__ = func.__name__
    wrap.__doc__ = func.__doc__
    return wrap


def login_required(func):
    def wrap(*args, **kwargs):
        if session["username"] is None:
            flash("Not logged in", "danger")
            return redirect(url_for("auth.login"))
        result = func(*args, **kwargs, user=get_user())
        return result

    wrap.__name__ = func.__name__
    wrap.__doc__ = func.__doc__
    return wrap
