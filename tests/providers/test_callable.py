"""Dependency injector callable providers unittests."""

import unittest2 as unittest

from dependency_injector import (
    providers,
    utils,
    errors,
)


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
        provider = providers.Callable(self.example) \
            .args(1, 2, 3, 4)

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_keyword_args(self):
        """Test call with keyword args.

        New simplified syntax.
        """
        provider = providers.Callable(self.example) \
            .kwargs(arg1=1, arg2=2, arg3=3, arg4=4)

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_positional_and_keyword_args(self):
        """Test call with positional and keyword args.

        Simplified syntax of positional and keyword arg injections.
        """
        provider = providers.Callable(self.example) \
            .args(1, 2) \
            .kwargs(arg3=3, arg4=4)

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_context_args(self):
        """Test call with context args."""
        provider = providers.Callable(self.example) \
            .args(1, 2)

        self.assertTupleEqual(provider(3, 4), (1, 2, 3, 4))

    def test_call_with_context_kwargs(self):
        """Test call with context kwargs."""
        provider = providers.Callable(self.example) \
            .kwargs(arg1=1)

        self.assertTupleEqual(provider(arg2=2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_call_with_context_args_and_kwargs(self):
        """Test call with context args and kwargs."""
        provider = providers.Callable(self.example) \
            .args(1)

        self.assertTupleEqual(provider(2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_call_overridden(self):
        """Test creation of new instances on overridden provider."""
        provider = providers.Callable(self.example)

        provider.override(providers.Object((4, 3, 2, 1)))
        provider.override(providers.Object((1, 2, 3, 4)))

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_injections(self):
        """Test getting a full list of injections using injections property."""
        provider = providers.Callable(self.example) \
            .args(1, 2) \
            .kwargs(arg3=3, arg4=4)

        self.assertEquals(len(provider.injections), 4)

    def test_repr(self):
        """Test representation of provider."""
        provider = providers.Callable(self.example) \
            .kwargs(arg1=providers.Factory(dict),
                    arg2=providers.Factory(list),
                    arg3=providers.Factory(set),
                    arg4=providers.Factory(tuple))

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
        self.assertTrue(utils.is_delegated_provider(
            providers.DelegatedCallable(len)))
        self.assertFalse(utils.is_delegated_provider(providers.Callable(len)))
