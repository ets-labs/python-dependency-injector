"""Application module."""

from flask import Flask
from flask_bootstrap import Bootstrap4

from .containers import Container
from . import views


def create_app() -> Flask:
    container = Container()
    container.config.github.auth_token.from_env("GITHUB_TOKEN")

    app = Flask(__name__)
    app.container = container
    app.add_url_rule("/", "index", views.index)

    bootstrap = Bootstrap4()
    bootstrap.init_app(app)

    return app
