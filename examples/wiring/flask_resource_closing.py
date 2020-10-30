"""`Resource` - Flask request scope example."""

import sys

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, Closing
from flask import Flask, current_app


class Service:
    ...


def init_service() -> Service:
    print('Init service')
    yield Service()
    print('Shutdown service')


class Container(containers.DeclarativeContainer):

    service = providers.Resource(init_service)


def index_view(service: Service = Closing[Provide[Container.service]]):
    assert service is current_app.container.service()
    return 'Hello  World!'


container = Container()
container.wire(modules=[sys.modules[__name__]])

app = Flask(__name__)
app.container = container
app.add_url_rule('/', 'index', view_func=index_view)


if __name__ == '__main__':
    app.run()
