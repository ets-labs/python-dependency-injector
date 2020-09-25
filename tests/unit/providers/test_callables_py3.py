"""Dependency injector callable providers unit tests."""

import sys

import unittest2 as unittest

from dependency_injector import (
    providers,
    errors,
)


def _example(arg1, arg2, arg3, arg4):
    return arg1, arg2, arg3, arg4


class CallableTests(unittest.TestCase):

    def test_init_with_callable(self):
        self.assertTrue(providers.Callable(_example))

    def test_init_with_not_callable(self):
        self.assertRaises(errors.Error, providers.Callable, 123)

    def test_provided_instance_provider(self):
        provider = providers.Callable(_example)
        self.assertIsInstance(provider.provided, providers.ProvidedInstance)

    def test_call(self):
        provider = providers.Callable(lambda: True)
        self.assertTrue(provider())

    def test_call_with_positional_args(self):
        provider = providers.Callable(_example,
                                      1, 2, 3, 4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_keyword_args(self):
        provider = providers.Callable(_example,
                                      arg1=1, arg2=2, arg3=3, arg4=4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_positional_and_keyword_args(self):
        provider = providers.Callable(_example,
                                      1, 2,
                                      arg3=3, arg4=4)
        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_call_with_context_args(self):
        provider = providers.Callable(_example, 1, 2)
        self.assertTupleEqual(provider(3, 4), (1, 2, 3, 4))

    def test_call_with_context_kwargs(self):
        provider = providers.Callable(_example, arg1=1)
        self.assertTupleEqual(provider(arg2=2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_call_with_context_args_and_kwargs(self):
        provider = providers.Callable(_example, 1)
        self.assertTupleEqual(provider(2, arg3=3, arg4=4), (1, 2, 3, 4))

    def test_fluent_interface(self):
        provider = providers.Singleton(_example) \
            .add_args(1, 2) \
            .add_kwargs(arg3=3, arg4=4)

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_set_args(self):
        provider = providers.Callable(_example) \
            .add_args(1, 2) \
            .set_args(3, 4)
        self.assertEqual(provider.args, tuple([3, 4]))

    def test_set_kwargs(self):
        provider = providers.Callable(_example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .set_kwargs(init_arg3=4, init_arg4=5)
        self.assertEqual(provider.kwargs, dict(init_arg3=4, init_arg4=5))

    def test_clear_args(self):
        provider = providers.Callable(_example) \
            .add_args(1, 2) \
            .clear_args()
        self.assertEqual(provider.args, tuple())

    def test_clear_kwargs(self):
        provider = providers.Callable(_example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .clear_kwargs()
        self.assertEqual(provider.kwargs, dict())

    def test_call_overridden(self):
        provider = providers.Callable(_example)

        provider.override(providers.Object((4, 3, 2, 1)))
        provider.override(providers.Object((1, 2, 3, 4)))

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_deepcopy(self):
        provider = providers.Callable(_example)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIs(provider.provides, provider_copy.provides)
        self.assertIsInstance(provider, providers.Callable)

    def test_deepcopy_from_memo(self):
        provider = providers.Callable(_example)
        provider_copy_memo = providers.Callable(_example)

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_args(self):
        provider = providers.Callable(_example)
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
        provider = providers.Callable(_example)
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
        provider = providers.Callable(_example)
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIs(provider.provides, provider_copy.provides)
        self.assertIsInstance(provider, providers.Callable)

        self.assertIsNot(object_provider, object_provider_copy)
        self.assertIsInstance(object_provider_copy, providers.Object)

    def test_deepcopy_with_sys_streams(self):
        provider = providers.Callable(_example)
        provider.add_args(sys.stdin)
        provider.add_kwargs(a2=sys.stdout)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider_copy, providers.Callable)
        self.assertIs(provider.args[0], sys.stdin)
        self.assertIs(provider.kwargs['a2'], sys.stdout)

    def test_repr(self):
        provider = providers.Callable(_example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'Callable({0}) at {1}>'.format(
                             repr(_example),
                             hex(id(provider))))


class DelegatedCallableTests(unittest.TestCase):

    def test_inheritance(self):
        self.assertIsInstance(providers.DelegatedCallable(_example),
                              providers.Callable)

    def test_is_provider(self):
        self.assertTrue(
            providers.is_provider(providers.DelegatedCallable(_example)))

    def test_is_delegated_provider(self):
        provider = providers.DelegatedCallable(_example)
        self.assertTrue(providers.is_delegated(provider))

    def test_repr(self):
        provider = providers.DelegatedCallable(_example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'DelegatedCallable({0}) at {1}>'.format(
                             repr(_example),
                             hex(id(provider))))


class AbstractCallableTests(unittest.TestCase):

    def test_inheritance(self):
        self.assertIsInstance(providers.AbstractCallable(_example),
                              providers.Callable)

    def test_call_overridden_by_callable(self):
        def _abstract_example():
            pass

        provider = providers.AbstractCallable(_abstract_example)
        provider.override(providers.Callable(_example))

        self.assertTrue(provider(1, 2, 3, 4), (1, 2, 3, 4))

    def test_call_overridden_by_delegated_callable(self):
        def _abstract_example():
            pass

        provider = providers.AbstractCallable(_abstract_example)
        provider.override(providers.DelegatedCallable(_example))

        self.assertTrue(provider(1, 2, 3, 4), (1, 2, 3, 4))

    def test_call_not_overridden(self):
        provider = providers.AbstractCallable(_example)

        with self.assertRaises(errors.Error):
            provider(1, 2, 3, 4)

    def test_override_by_not_callable(self):
        provider = providers.AbstractCallable(_example)

        with self.assertRaises(errors.Error):
            provider.override(providers.Factory(object))

    def test_provide_not_implemented(self):
        provider = providers.AbstractCallable(_example)

        with self.assertRaises(NotImplementedError):
            provider._provide((1, 2, 3, 4), dict())

    def test_repr(self):
        provider = providers.AbstractCallable(_example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'AbstractCallable({0}) at {1}>'.format(
                             repr(_example),
                             hex(id(provider))))


class CallableDelegateTests(unittest.TestCase):

    def setUp(self):
        self.delegated = providers.Callable(_example)
        self.delegate = providers.CallableDelegate(self.delegated)

    def test_is_delegate(self):
        self.assertIsInstance(self.delegate, providers.Delegate)

    def test_init_with_not_callable(self):
        self.assertRaises(errors.Error,
                          providers.CallableDelegate,
                          providers.Object(object()))
