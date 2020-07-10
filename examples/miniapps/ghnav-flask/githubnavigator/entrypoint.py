"""Entrypoint module."""

from .application import Application


application = Application()
application.config.from_yaml('config.yml')
application.config.github.auth_token.from_env('GITHUB_TOKEN')
app = application.app()
