from django.apps import AppConfig

from githubnavigator import container
from . import views


class WebConfig(AppConfig):
    name = 'githubnavigator.web'

    def ready(self):
        container.wire(modules=[views])
