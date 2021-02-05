"""Dependency injector provided instance provider unit tests."""

import unittest2 as unittest

from dependency_injector import containers, providers


class Service:
    def __init__(self, value):
        self.value = value
        self.values = [self.value]

    def __call__(self):
        return self.value

    def __getitem__(self, item):
        return self.values[item]

    def get_value(self):
        return self.value

    def get_closure(self):
        def closure():
            return self.value
        return closure


class Client:
    def __init__(self, value):
        self.value = value


class Container(containers.DeclarativeContainer):

    service = providers.Singleton(Service, value='foo')

    client_attribute = providers.Factory(
        Client,
        value=service.provided.value,
    )

    client_item = providers.Factory(
        Client,
        value=service.provided[0],
    )

    client_attribute_item = providers.Factory(
        Client,
        value=service.provided.values[0],
    )

    client_method_call = providers.Factory(
        Client,
        value=service.provided.get_value.call(),
    )
    client_method_closure_call = providers.Factory(
        Client,
        value=service.provided.get_closure.call().call(),
    )

    client_provided_call = providers.Factory(
        Client,
        value=service.provided.call(),
    )


class ProvidedInstanceTests(unittest.TestCase):

    def setUp(self):
        self.container = Container()

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.container.service.provided))

    def test_attribute(self):
        client = self.container.client_attribute()
        self.assertEqual(client.value, 'foo')

    def test_item(self):
        client = self.container.client_item()
        self.assertEqual(client.value, 'foo')

    def test_attribute_item(self):
        client = self.container.client_attribute_item()
        self.assertEqual(client.value, 'foo')

    def test_method_call(self):
        client = self.container.client_method_call()
        self.assertEqual(client.value, 'foo')

    def test_method_closure_call(self):
        client = self.container.client_method_closure_call()
        self.assertEqual(client.value, 'foo')

    def test_provided_call(self):
        client = self.container.client_provided_call()
        self.assertEqual(client.value, 'foo')

    def test_call_overridden(self):
        value = 'bar'
        with self.container.service.override(Service(value)):
            self.assertEqual(self.container.client_attribute().value, value)
            self.assertEqual(self.container.client_item().value, value)
            self.assertEqual(self.container.client_attribute_item().value, value)
            self.assertEqual(self.container.client_method_call().value, value)

    def test_repr_provided_instance(self):
        provider = self.container.service.provided
        self.assertEqual(
            'ProvidedInstance(\'{0}\')'.format(repr(self.container.service)),
            repr(provider),
        )

    def test_repr_attribute_getter(self):
        provider = self.container.service.provided.value
        self.assertEqual(
            'AttributeGetter(\'value\')',
            repr(provider),
        )

    def test_repr_item_getter(self):
        provider = self.container.service.provided['test-test']
        self.assertEqual(
            'ItemGetter(\'test-test\')',
            repr(provider),
        )


class ProvidedInstancePuzzleTests(unittest.TestCase):

    def test_puzzled(self):
        service = providers.Singleton(Service, value='foo-bar')

        dependency = providers.Object(
            {
                'a': {
                    'b': {
                        'c1': 10,
                        'c2': lambda arg: {'arg': arg}
                    },
                },
            },
        )

        test_list = providers.List(
            dependency.provided['a']['b']['c1'],
            dependency.provided['a']['b']['c2'].call(22)['arg'],
            dependency.provided['a']['b']['c2'].call(service)['arg'],
            dependency.provided['a']['b']['c2'].call(service)['arg'].value,
            dependency.provided['a']['b']['c2'].call(service)['arg'].get_value.call(),
        )

        result = test_list()

        self.assertEqual(
            result,
            [
                10,
                22,
                service(),
                'foo-bar',
                'foo-bar',
            ],
        )


class ProvidedInstanceInBaseClassTests(unittest.TestCase):

    def test_provided_attribute(self):
        provider = providers.Provider()
        assert isinstance(provider.provided, providers.ProvidedInstance)
