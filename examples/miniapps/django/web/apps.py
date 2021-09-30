"""Application config module."""

from django.apps import AppConfig

from githubnavigator import container


class WebConfig(AppConfig):
    name = "web"

    def ready(self):
        container.wire(modules=[".views"])
