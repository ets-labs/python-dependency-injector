"""Dependency injector callable providers unittests."""

import unittest2 as unittest

from dependency_injector import providers, errors


class CallableTests(unittest.TestCase):

    def example(self, arg1, arg2, arg3, arg4):
        return arg1, arg2, arg3, arg4

    def test_init_with_callable(self):
        self.assertTrue(providers.Callable(self.example))

    def test_init_with_not_callable(self):
        self.assertRaises(errors.Error, providers.Callable, 123)

    def test_call(self):
        provider = providers.Callable(lambda: True)
        self.assertTrue(provider())

    def test_call_with_positional_args(self):
        provider = providers.Callable(self.example,
                                      1, 2, 3, 4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_keyword_args(self):
        provider = providers.Callable(self.example,
                                      arg1=1, arg2=2, arg3=3, arg4=4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_positional_and_keyword_args(self):
        provider = providers.Callable(self.example,
                                      1, 2,
                                      arg3=3, arg4=4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_context_args(self):
        provider = providers.Callable(self.example, 1, 2)
        self.assertTupleEqual(provider(3, 4), (1, 2, 3, 4))

    def test_call_with_context_kwargs(self):
        provider = providers.Callable(self.example, arg1=1)
        self.assertTupleEqual(provider(arg2=2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_call_with_context_args_and_kwargs(self):
        provider = providers.Callable(self.example, 1)
        self.assertTupleEqual(provider(2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_fluent_interface(self):
        provider = providers.Singleton(self.example) \
            .add_args(1, 2) \
            .add_kwargs(arg3=3, arg4=4)

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_overridden(self):
        provider = providers.Callable(self.example)

        provider.override(providers.Object((4, 3, 2, 1)))
        provider.override(providers.Object((1, 2, 3, 4)))

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_repr(self):
        provider = providers.Callable(self.example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.callable.'
                         'Callable({0}) at {1}>'.format(
                             repr(self.example),
                             hex(id(provider))))


class DelegatedCallableTests(unittest.TestCase):

    def test_inheritance(self):
        self.assertIsInstance(providers.DelegatedCallable(len),
                              providers.Callable)

    def test_is_provider(self):
        self.assertTrue(
            providers.is_provider(providers.DelegatedCallable(len)))

    def test_is_delegated_provider(self):
        provider = providers.DelegatedCallable(len)
        self.assertIs(provider.provide_injection(), provider)
