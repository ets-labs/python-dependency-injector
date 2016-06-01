"""Dependency injector callable providers unittests."""

import unittest2 as unittest

from dependency_injector import providers, utils, errors


class CallableTests(unittest.TestCase):
    """Callable test cases."""

    def example(self, arg1, arg2, arg3, arg4):
        """Example callback."""
        return arg1, arg2, arg3, arg4

    def test_init_with_callable(self):
        """Test creation of provider with a callable."""
        self.assertTrue(providers.Callable(self.example))

    def test_init_with_not_callable(self):
        """Test creation of provider with not a callable."""
        self.assertRaises(errors.Error, providers.Callable, 123)

    def test_call(self):
        """Test call."""
        provider = providers.Callable(lambda: True)
        self.assertTrue(provider())

    def test_call_with_positional_args(self):
        """Test call with positional args.

        New simplified syntax.
        """
        provider = providers.Callable(self.example,
                                      1, 2, 3, 4)

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_keyword_args(self):
        """Test call with keyword args."""
        provider = providers.Callable(self.example,
                                      arg1=1, arg2=2, arg3=3, arg4=4)

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_positional_and_keyword_args(self):
        """Test call with positional and keyword args."""
        provider = providers.Callable(self.example,
                                      1, 2,
                                      arg3=3, arg4=4)

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_context_args(self):
        """Test call with context args."""
        provider = providers.Callable(self.example, 1, 2)

        self.assertTupleEqual(provider(3, 4), (1, 2, 3, 4))

    def test_call_with_context_kwargs(self):
        """Test call with context kwargs."""
        provider = providers.Callable(self.example, arg1=1)

        self.assertTupleEqual(provider(arg2=2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_call_with_context_args_and_kwargs(self):
        """Test call with context args and kwargs."""
        provider = providers.Callable(self.example, 1)

        self.assertTupleEqual(provider(2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_fluent_interface(self):
        """Test injections definition with fluent interface."""
        provider = providers.Singleton(self.example) \
            .add_args(1, 2) \
            .add_kwargs(arg3=3, arg4=4) \

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_overridden(self):
        """Test creation of new instances on overridden provider."""
        provider = providers.Callable(self.example)

        provider.override(providers.Object((4, 3, 2, 1)))
        provider.override(providers.Object((1, 2, 3, 4)))

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_repr(self):
        """Test representation of provider."""
        provider = providers.Callable(self.example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.callable.'
                         'Callable({0}) at {1}>'.format(
                             repr(self.example),
                             hex(id(provider))))


class DelegatedCallableTests(unittest.TestCase):
    """DelegatedCallable test cases."""

    def test_inheritance(self):
        """Test inheritance."""
        self.assertIsInstance(providers.DelegatedCallable(len),
                              providers.Callable)

    def test_is_provider(self):
        """Test is_provider."""
        self.assertTrue(utils.is_provider(providers.DelegatedCallable(len)))

    def test_is_delegated_provider(self):
        """Test is_delegated_provider."""
        provider = providers.DelegatedCallable(len)
        self.assertIs(provider.provide_injection(), provider)
