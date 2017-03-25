"""Dependency injector callable providers unit tests."""

import unittest2 as unittest

from dependency_injector import (
    providers,
    errors,
)


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

    def test_set_args(self):
        provider = providers.Callable(self.example) \
            .add_args(1, 2) \
            .set_args(3, 4)
        self.assertEqual(provider.args, tuple([3, 4]))

    def test_set_kwargs(self):
        provider = providers.Callable(self.example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .set_kwargs(init_arg3=4, init_arg4=5)
        self.assertEqual(provider.kwargs, dict(init_arg3=4, init_arg4=5))

    def test_clear_args(self):
        provider = providers.Callable(self.example) \
            .add_args(1, 2) \
            .clear_args()
        self.assertEqual(provider.args, tuple())

    def test_clear_kwargs(self):
        provider = providers.Callable(self.example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .clear_kwargs()
        self.assertEqual(provider.kwargs, dict())

    def test_call_overridden(self):
        provider = providers.Callable(self.example)

        provider.override(providers.Object((4, 3, 2, 1)))
        provider.override(providers.Object((1, 2, 3, 4)))

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_deepcopy(self):
        provider = providers.Callable(self.example)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIs(provider.provides, provider_copy.provides)
        self.assertIsInstance(provider, providers.Callable)

    def test_deepcopy_from_memo(self):
        provider = providers.Callable(self.example)
        provider_copy_memo = providers.Callable(self.example)

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_args(self):
        provider = providers.Callable(self.example)
        dependent_provider1 = providers.Callable(list)
        dependent_provider2 = providers.Callable(dict)

        provider.add_args(dependent_provider1, dependent_provider2)

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.args[0]
        dependent_provider_copy2 = provider_copy.args[1]

        self.assertNotEqual(provider.args, provider_copy.args)

        self.assertIs(dependent_provider1.provides,
                      dependent_provider_copy1.provides)
        self.assertIsNot(dependent_provider1, dependent_provider_copy1)

        self.assertIs(dependent_provider2.provides,
                      dependent_provider_copy2.provides)
        self.assertIsNot(dependent_provider2, dependent_provider_copy2)

    def test_deepcopy_kwargs(self):
        provider = providers.Callable(self.example)
        dependent_provider1 = providers.Callable(list)
        dependent_provider2 = providers.Callable(dict)

        provider.add_kwargs(a1=dependent_provider1, a2=dependent_provider2)

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.kwargs['a1']
        dependent_provider_copy2 = provider_copy.kwargs['a2']

        self.assertNotEqual(provider.kwargs, provider_copy.kwargs)

        self.assertIs(dependent_provider1.provides,
                      dependent_provider_copy1.provides)
        self.assertIsNot(dependent_provider1, dependent_provider_copy1)

        self.assertIs(dependent_provider2.provides,
                      dependent_provider_copy2.provides)
        self.assertIsNot(dependent_provider2, dependent_provider_copy2)

    def test_deepcopy_overridden(self):
        provider = providers.Callable(self.example)
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIs(provider.provides, provider_copy.provides)
        self.assertIsInstance(provider, providers.Callable)

        self.assertIsNot(object_provider, object_provider_copy)
        self.assertIsInstance(object_provider_copy, providers.Object)

    def test_repr(self):
        provider = providers.Callable(self.example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
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
        self.assertTrue(providers.is_delegated(provider))

    def test_repr(self):
        provider = providers.DelegatedCallable(len)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'DelegatedCallable({0}) at {1}>'.format(
                             repr(len),
                             hex(id(provider))))
