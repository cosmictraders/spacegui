import autotraders.token
from autotraders.agent import Agent
from flask import render_template

from website.model import db, User
from website.session import get_session, get_token
from minify_html import minify
from autotraders.session import AutoTradersSession as AutotradersSession


def minify_html(func):
    def wrap(*args, **kwargs):
        result: str = func(*args, **kwargs)
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

    wrap.__name__ = func.__name__
    wrap.__doc__ = func.__doc__
    return wrap


def token_required(func):
    def wrap(*args, **kwargs):
        try:
            session = get_session()
            token = get_token()
            parsed_token = autotraders.token.parse_token(token)
            # parsed_token.payload.reset_date
        except Exception as e:
            print(e)
            db.create_all()

            class MockAgent:
                def __init__(self, token, id, active):
                    self.token = token
                    self.id = id
                    self.active = active

            users = []
            for user in db.session.query(User).all():
                try:
                    a = Agent(AutotradersSession(user.token))
                    a.active = user.active
                    a.id = user.id
                    users.append(a)
                except Exception as e:
                    users.append(MockAgent(user.token, user.id, user.active))
            return render_template("local/select_user.html", users=users)
        result = func(*args, **kwargs, session=session)
        return result

    wrap.__name__ = func.__name__
    wrap.__doc__ = func.__doc__
    return wrap
