"""Dependency injector Flask extension unit tests."""

import unittest2 as unittest
from flask import Flask, url_for
from flask.views import MethodView

from dependency_injector import containers
from dependency_injector.ext import flask


def index():
    return 'Hello World!'


def test():
    return 'Test!'


class Test(MethodView):
    def get(self):
        return 'Test class-based!'


class ApplicationContainer(containers.DeclarativeContainer):

    app = flask.Application(Flask, __name__)

    index_view = flask.View(index)
    test_view = flask.View(test)
    test_class_view = flask.ClassBasedView(Test)


def create_app():
    container = ApplicationContainer()
    app = container.app()
    app.container = container
    app.add_url_rule('/', view_func=container.index_view.as_view())
    app.add_url_rule('/test', 'test-test', view_func=container.test_view.as_view())
    app.add_url_rule('/test-class', view_func=container.test_class_view.as_view('test-class'))
    return app


class ApplicationTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['SERVER_NAME'] = 'test-server.com'
        self.client = self.app.test_client()
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None, None, None)

    def test_index(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello World!')

    def test_test(self):
        response = self.client.get('/test')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Test!')

    def test_test_class_based(self):
        response = self.client.get('/test-class')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Test class-based!')

    def test_endpoints(self):
        with self.app.app_context():
            self.assertEqual(url_for('index'), 'http://test-server.com/')
            self.assertEqual(url_for('test-test'), 'http://test-server.com/test')
            self.assertEqual(url_for('test-class'), 'http://test-server.com/test-class')
