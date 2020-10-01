from django.apps import AppConfig
from django.conf import settings

from githubnavigator import container
from . import views


class WebConfig(AppConfig):
    name = 'web'

    def ready(self):
        container.wire(modules=[views])
