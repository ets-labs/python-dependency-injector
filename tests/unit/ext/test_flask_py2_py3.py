"""Dependency injector Flask extension unit tests."""

import unittest2 as unittest
from flask import url_for
from flask.views import MethodView

from dependency_injector import containers, providers
from dependency_injector.ext import flask


def index():
    return 'Hello World!'


def test():
    return 'Test!'


class Test(MethodView):
    def get(self):
        return 'Test class-based!'


class Application(containers.DeclarativeContainer):

    index_view = providers.Callable(index)
    test_view = providers.Callable(test)
    test_class_view = providers.Factory(Test)

    app = providers.Factory(
        flask.create_app,
        name=__name__,
        routes=[
            flask.Route('/', view_provider=index_view),
            flask.Route('/test', 'test-test', test_view),
            flask.Route('/test-class', 'test-class', test_class_view)
        ],
    )


class ApplicationTests(unittest.TestCase):

    def setUp(self):
        application = Application()
        self.app = application.app()
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
