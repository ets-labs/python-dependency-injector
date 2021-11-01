"""Flask extension tests."""

from dependency_injector import containers
from dependency_injector.ext import flask
from flask import Flask, url_for
from flask.views import MethodView
from pytest import fixture


def index():
    return "Hello World!"


def test():
    return "Test!"


class Test(MethodView):
    def get(self):
        return "Test class-based!"


class ApplicationContainer(containers.DeclarativeContainer):

    app = flask.Application(Flask, __name__)

    index_view = flask.View(index)
    test_view = flask.View(test)
    test_class_view = flask.ClassBasedView(Test)


@fixture
def app():
    container = ApplicationContainer()
    app = container.app()
    app.container = container
    app.config["SERVER_NAME"] = "test-server.com"
    app.add_url_rule("/", view_func=container.index_view.as_view())
    app.add_url_rule("/test", "test-test", view_func=container.test_view.as_view())
    app.add_url_rule("/test-class", view_func=container.test_class_view.as_view("test-class"))
    return app


@fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.data == b"Hello World!"


def test_test(client):
    response = client.get("/test")

    assert response.status_code == 200
    assert response.data == b"Test!"


def test_test_class_based(client):
    response = client.get("/test-class")

    assert response.status_code == 200
    assert response.data == b"Test class-based!"


def test_endpoints(app):
    with app.app_context():
        assert url_for("index") == "http://test-server.com/"
        assert url_for("test-test") == "http://test-server.com/test"
        assert url_for("test-class") == "http://test-server.com/test-class"
