import unittest

from dependency_injector import containers


class SomeClass:
    ...


class TypesTest(unittest.TestCase):

    def test_declarative(self):
        container: containers.Container = containers.DeclarativeContainer()
        self.assertIsInstance(container, containers.Container)

    def test_dynamic(self):
        container: containers.Container = containers.DynamicContainer()
        self.assertIsInstance(container, containers.Container)
