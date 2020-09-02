"""`Singleton` - Flask request scope example."""

from dependency_injector import providers
from flask import Flask


class Service:
    ...


service_provider = providers.Singleton(Service)


def index_view():
    service_1 = service_provider()
    service_2 = service_provider()
    assert service_1 is service_2
    print(service_1)
    return 'Hello  World!'


def teardown_context(request):
    service_provider.reset()
    return request


app = Flask(__name__)
app.add_url_rule('/', 'index', view_func=index_view)
app.after_request(teardown_context)


if __name__ == '__main__':
    app.run()
