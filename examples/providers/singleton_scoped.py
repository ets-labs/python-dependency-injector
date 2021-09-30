"""`Singleton` - Flask request scope example."""

from dependency_injector import containers, providers
from flask import Flask, current_app


class Service:
    ...


class Container(containers.DeclarativeContainer):

    service_provider = providers.ThreadLocalSingleton(Service)


def index_view():
    service_1 = current_app.container.service_provider()
    service_2 = current_app.container.service_provider()
    assert service_1 is service_2
    print(service_1)
    return "Hello  World!"


def teardown_context(request):
    current_app.container.service_provider.reset()
    return request


container = Container()

app = Flask(__name__)
app.container = container
app.add_url_rule("/", "index", view_func=index_view)
app.after_request(teardown_context)


if __name__ == "__main__":
    app.run()
