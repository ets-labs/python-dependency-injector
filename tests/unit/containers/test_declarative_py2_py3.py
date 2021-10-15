"""Dependency injector declarative container unit tests."""

import unittest

from dependency_injector import (
    containers,
    providers,
)


class DeclarativeContainerWithCustomStringTests(unittest.TestCase):
    # See: https://github.com/ets-labs/python-dependency-injector/issues/479

    class CustomString(str):
        pass

    class CustomClass:
        thing = None

    class CustomContainer(containers.DeclarativeContainer):
        pass

    def setUp(self):
        self.container = self.CustomContainer
        self.provider = providers.Provider()

    def test_setattr(self):
        setattr(self.container, self.CustomString("test_attr"), self.provider)
        self.assertIs(self.container.test_attr, self.provider)

    def test_delattr(self):
        setattr(self.container, self.CustomString("test_attr"), self.provider)
        delattr(self.container, self.CustomString("test_attr"))
        with self.assertRaises(AttributeError):
            self.container.test_attr
