"""Dependency injector singleton providers unit tests."""

import unittest

from dependency_injector import (
    providers,
    errors,
)
from pytest import raises

from .singleton_common import Example, _BaseSingletonTestCase


class SingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.Singleton

    def test_repr(self):
        provider = self.singleton_cls(Example)
        assert repr(provider) == (
            "<dependency_injector.providers."
            "Singleton({0}) at {1}>".format(repr(Example), hex(id(provider)))
        )


class DelegatedSingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.DelegatedSingleton

    def test_is_delegated_provider(self):
        provider = self.singleton_cls(object)
        assert providers.is_delegated(provider) is True

    def test_repr(self):
        provider = self.singleton_cls(Example)
        assert repr(provider) == (
            "<dependency_injector.providers."
            "DelegatedSingleton({0}) at {1}>".format(repr(Example), hex(id(provider)))
        )


class ThreadLocalSingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.ThreadLocalSingleton

    def test_repr(self):
        provider = providers.ThreadLocalSingleton(Example)
        assert repr(provider) == (
            "<dependency_injector.providers."
            "ThreadLocalSingleton({0}) at {1}>".format(repr(Example), hex(id(provider)))
        )

    def test_reset(self):
        provider = providers.ThreadLocalSingleton(Example)

        instance1 = provider()
        assert isinstance(instance1, Example)

        provider.reset()

        instance2 = provider()
        assert isinstance(instance2, Example)

        assert instance1 is not instance2

    def test_reset_clean(self):
        provider = providers.ThreadLocalSingleton(Example)
        instance1 = provider()

        provider.reset()
        provider.reset()

        instance2 = provider()
        assert instance1 is not instance2


class DelegatedThreadLocalSingletonTests(_BaseSingletonTestCase,
                                         unittest.TestCase):

    singleton_cls = providers.DelegatedThreadLocalSingleton

    def test_is_delegated_provider(self):
        provider = self.singleton_cls(object)
        assert providers.is_delegated(provider) is True

    def test_repr(self):
        provider = self.singleton_cls(Example)

        assert repr(provider) == (
            "<dependency_injector.providers."
            "DelegatedThreadLocalSingleton({0}) at {1}>".format(repr(Example), hex(id(provider)))
        )


class ThreadSafeSingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.ThreadSafeSingleton

    def test_repr(self):
        provider = self.singleton_cls(Example)
        assert repr(provider) == (
            "<dependency_injector.providers."
            "ThreadSafeSingleton({0}) at {1}>".format(repr(Example), hex(id(provider)))
        )


class DelegatedThreadSafeSingletonTests(_BaseSingletonTestCase,
                                        unittest.TestCase):

    singleton_cls = providers.DelegatedThreadSafeSingleton

    def test_is_delegated_provider(self):
        provider = self.singleton_cls(object)
        assert providers.is_delegated(provider) is True

    def test_repr(self):
        provider = self.singleton_cls(Example)
        assert repr(provider) == (
            "<dependency_injector.providers."
            "DelegatedThreadSafeSingleton({0}) at {1}>".format(repr(Example), hex(id(provider)))
        )


class AbstractSingletonTests(unittest.TestCase):

    def test_inheritance(self):
        assert isinstance(providers.AbstractSingleton(Example),
                              providers.BaseSingleton)

    def test_call_overridden_by_singleton(self):
        provider = providers.AbstractSingleton(object)
        provider.override(providers.Singleton(Example))

        assert isinstance(provider(), Example)

    def test_call_overridden_by_delegated_singleton(self):
        provider = providers.AbstractSingleton(object)
        provider.override(providers.DelegatedSingleton(Example))

        assert isinstance(provider(), Example)

    def test_call_not_overridden(self):
        provider = providers.AbstractSingleton(object)

        with raises(errors.Error):
            provider()

    def test_reset_overridden(self):
        provider = providers.AbstractSingleton(object)
        provider.override(providers.Singleton(Example))

        instance1 = provider()

        provider.reset()

        instance2 = provider()

        assert instance1 is not instance2
        assert isinstance(instance1, Example)
        assert isinstance(instance2, Example)

    def test_reset_not_overridden(self):
        provider = providers.AbstractSingleton(object)

        with raises(errors.Error):
            provider.reset()

    def test_override_by_not_singleton(self):
        provider = providers.AbstractSingleton(object)

        with raises(errors.Error):
            provider.override(providers.Factory(object))

    def test_repr(self):
        provider = providers.AbstractSingleton(Example)
        assert repr(provider) == (
            "<dependency_injector.providers."
            "AbstractSingleton({0}) at {1}>".format(repr(Example), hex(id(provider)))
        )


class SingletonDelegateTests(unittest.TestCase):

    def setUp(self):
        self.delegated = providers.Singleton(Example)
        self.delegate = providers.SingletonDelegate(self.delegated)

    def test_is_delegate(self):
        assert isinstance(self.delegate, providers.Delegate)

    def test_init_with_not_singleton(self):
        raises(errors.Error,
                          providers.SingletonDelegate,
                          providers.Object(object()))
