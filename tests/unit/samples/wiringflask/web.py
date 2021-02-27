import sys

from flask import Flask, jsonify, request, current_app, session, g
from flask import _request_ctx_stack, _app_ctx_stack
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

# This is here for testing wiring bypasses these objects without crashing
request, current_app, session, g  # noqa
_request_ctx_stack, _app_ctx_stack  # noqa


class Service:
    def process(self) -> str:
        return 'Ok'


class Container(containers.DeclarativeContainer):

    service = providers.Factory(Service)


app = Flask(__name__)


@app.route('/')
@inject
def index(service: Service = Provide[Container.service]):
    result = service.process()
    return jsonify({'result': result})


container = Container()
container.wire(modules=[sys.modules[__name__]])
