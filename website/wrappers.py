import flask
from flask import render_template

from website.model import db
from website.session import get_session
from minify_html import minify


def minify_html(func):
    def wrap(*args, **kwargs):
        result: str = func(*args, **kwargs)  # TODO: Fix
        return minify(result, do_not_minify_doctype=True,
                      ensure_spec_compliant_unquoted_attribute_values=True,
                      keep_closing_tags=True,
                      keep_comments=False,
                      keep_html_and_head_opening_tags=True,
                      keep_spaces_between_attributes=True,
                      minify_css=True,
                      minify_js=False,
                      remove_bangs=False,
                      remove_processing_instructions=False
                      )

    wrap.__name__ = func.__name__
    wrap.__doc__ = func.__doc__
    return wrap


def token_required(func):
    """Decorator that reports the execution time."""

    def wrap(*args, **kwargs):
        try:
            session = get_session()
            result = func(*args, **kwargs, session=session)
            return result
        except Exception as e:
            print(e)
            db.create_all()
            return render_template("setup.html")

    wrap.__name__ = func.__name__
    wrap.__doc__ = func.__doc__
    return wrap
