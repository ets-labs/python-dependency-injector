"""Entrypoint module."""

from .application import Application


application = Application()
application.config.from_yaml('config.yml')
app = application.app()
