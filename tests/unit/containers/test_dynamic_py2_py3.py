"""Dependency injector dynamic container unit tests."""

import unittest

from dependency_injector import (
    containers,
    providers,
)


class DynamicContainerWithCustomStringTests(unittest.TestCase):
    # See: https://github.com/ets-labs/python-dependency-injector/issues/479

    class CustomString(str):
        pass

    class CustomClass:
        thing = None

    def setUp(self):
        self.container = containers.DynamicContainer()
        self.provider = providers.Provider()

    def test_setattr(self):
        setattr(self.container, self.CustomString("test_attr"), self.provider)
        self.assertIs(self.container.test_attr, self.provider)

    def test_delattr(self):
        setattr(self.container, self.CustomString("test_attr"), self.provider)
        delattr(self.container, self.CustomString("test_attr"))
        with self.assertRaises(AttributeError):
            self.container.test_attr

    def test_set_provider(self):
        self.container.set_provider(self.CustomString("test_attr"), self.provider)
        self.assertIs(self.container.test_attr, self.provider)

    def test_set_providers(self):
        self.container.set_providers(**{self.CustomString("test_attr"): self.provider})
        self.assertIs(self.container.test_attr, self.provider)
