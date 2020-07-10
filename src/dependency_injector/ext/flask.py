"""Flask extension module."""

from flask import Flask


def create_app(name, routes):
    app = Flask(name)
    for route in routes:
        app.add_url_rule(*route.args, **route.kwargs)
    return app


class Route:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
