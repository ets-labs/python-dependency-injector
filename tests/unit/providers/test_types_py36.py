import unittest

from dependency_injector import providers, types


class SomeClass:
    ...


class TypesTest(unittest.TestCase):

    def test_provider(self):
        provider: types.Provider[SomeClass] = providers.Factory(SomeClass)
        some_object = provider()
        self.assertIsInstance(some_object, SomeClass)
