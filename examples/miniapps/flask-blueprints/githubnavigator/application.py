"""Application module."""

from flask import Flask
from flask_bootstrap import Bootstrap

from .containers import Container
from .blueprints import example


def create_app() -> Flask:
    container = Container()
    container.config.github.auth_token.from_env("GITHUB_TOKEN")

    app = Flask(__name__)
    app.container = container
    app.register_blueprint(example.blueprint)

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    return app
