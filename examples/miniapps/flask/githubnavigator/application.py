"""Application module."""

from flask import Flask
from flask_bootstrap import Bootstrap

from .containers import Container
from . import views


def create_app():
    container = Container()
    container.config.from_yaml('config.yml')
    container.config.github.auth_token.from_env('GITHUB_TOKEN')

    container.wire(modules=[views])

    app = Flask(__name__)
    app.container = container

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    app.add_url_rule('/', 'index', views.index)

    return app
