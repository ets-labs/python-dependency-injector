"""Dependency injector coroutine providers unit tests."""

import asyncio

import unittest2 as unittest

from dependency_injector import (
    providers,
    errors,
)


@asyncio.coroutine
def _example(arg1, arg2, arg3, arg4):
    future = asyncio.Future()
    future.set_result(None)
    yield from future
    return arg1, arg2, arg3, arg4


def _run(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


class CoroutineTests(unittest.TestCase):

    def test_init_with_coroutine(self):
        self.assertTrue(providers.Coroutine(_example))

    def test_init_with_not_coroutine(self):
        self.assertRaises(errors.Error, providers.Coroutine, lambda: None)

    def test_call_with_positional_args(self):
        provider = providers.Coroutine(_example, 1, 2, 3, 4)
        self.assertTupleEqual(_run(provider()), (1, 2, 3, 4))

    def test_call_with_keyword_args(self):
        provider = providers.Coroutine(_example,
                                       arg1=1, arg2=2, arg3=3, arg4=4)
        self.assertTupleEqual(_run(provider()), (1, 2, 3, 4))

    def test_call_with_positional_and_keyword_args(self):
        provider = providers.Coroutine(_example,
                                       1, 2,
                                       arg3=3, arg4=4)
        self.assertTupleEqual(_run(provider()), (1, 2, 3, 4))

    def test_call_with_context_args(self):
        provider = providers.Coroutine(_example, 1, 2)
        self.assertTupleEqual(_run(provider(3, 4)), (1, 2, 3, 4))

    def test_call_with_context_kwargs(self):
        provider = providers.Coroutine(_example, arg1=1)
        self.assertTupleEqual(
            _run(provider(arg2=2, arg3=3, arg4=4)),
            (1, 2, 3, 4),
        )

    def test_call_with_context_args_and_kwargs(self):
        provider = providers.Coroutine(_example, 1)
        self.assertTupleEqual(
            _run(provider(2, arg3=3, arg4=4)),
            (1, 2, 3, 4),
        )

    def test_fluent_interface(self):
        provider = providers.Coroutine(_example) \
            .add_args(1, 2) \
            .add_kwargs(arg3=3, arg4=4)

        self.assertTupleEqual(_run(provider()), (1, 2, 3, 4))

    def test_set_args(self):
        provider = providers.Coroutine(_example) \
            .add_args(1, 2) \
            .set_args(3, 4)
        self.assertEqual(provider.args, tuple([3, 4]))

    def test_set_kwargs(self):
        provider = providers.Coroutine(_example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .set_kwargs(init_arg3=4, init_arg4=5)
        self.assertEqual(provider.kwargs, dict(init_arg3=4, init_arg4=5))

    def test_clear_args(self):
        provider = providers.Coroutine(_example) \
            .add_args(1, 2) \
            .clear_args()
        self.assertEqual(provider.args, tuple())

    def test_clear_kwargs(self):
        provider = providers.Coroutine(_example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .clear_kwargs()
        self.assertEqual(provider.kwargs, dict())

    def test_call_overridden(self):
        provider = providers.Coroutine(_example)

        provider.override(providers.Object((4, 3, 2, 1)))
        provider.override(providers.Object((1, 2, 3, 4)))

        self.assertTupleEqual(provider(), (1, 2, 3, 4))

    def test_deepcopy(self):
        provider = providers.Coroutine(_example)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIs(provider.provides, provider_copy.provides)
        self.assertIsInstance(provider, providers.Coroutine)

    def test_deepcopy_from_memo(self):
        provider = providers.Coroutine(_example)
        provider_copy_memo = providers.Coroutine(_example)

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_args(self):
        provider = providers.Coroutine(_example)
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
        provider = providers.Coroutine(_example)
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
        provider = providers.Coroutine(_example)
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
        provider = providers.Coroutine(_example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'Coroutine({0}) at {1}>'.format(
                             repr(_example),
                             hex(id(provider))))


class DelegatedCoroutineTests(unittest.TestCase):

    def test_inheritance(self):
        self.assertIsInstance(providers.DelegatedCoroutine(_example),
                              providers.Coroutine)

    def test_is_provider(self):
        self.assertTrue(
            providers.is_provider(providers.DelegatedCoroutine(_example)))

    def test_is_delegated_provider(self):
        provider = providers.DelegatedCoroutine(_example)
        self.assertTrue(providers.is_delegated(provider))

    def test_repr(self):
        provider = providers.DelegatedCoroutine(_example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'DelegatedCoroutine({0}) at {1}>'.format(
                             repr(_example),
                             hex(id(provider))))


class AbstractCoroutineTests(unittest.TestCase):

    def test_inheritance(self):
        self.assertIsInstance(providers.AbstractCoroutine(_example),
                              providers.Coroutine)

    def test_call_overridden_by_coroutine(self):
        @asyncio.coroutine
        def _abstract_example():
            raise RuntimeError('Should not be raised')

        provider = providers.AbstractCoroutine(_abstract_example)
        provider.override(providers.Coroutine(_example))

        self.assertTrue(_run(provider(1, 2, 3, 4)), (1, 2, 3, 4))

    def test_call_overridden_by_delegated_coroutine(self):
        @asyncio.coroutine
        def _abstract_example():
            raise RuntimeError('Should not be raised')

        provider = providers.AbstractCoroutine(_abstract_example)
        provider.override(providers.DelegatedCoroutine(_example))

        self.assertTrue(_run(provider(1, 2, 3, 4)), (1, 2, 3, 4))

    def test_call_not_overridden(self):
        provider = providers.AbstractCoroutine(_example)

        with self.assertRaises(errors.Error):
            provider(1, 2, 3, 4)

    def test_override_by_not_coroutine(self):
        provider = providers.AbstractCoroutine(_example)

        with self.assertRaises(errors.Error):
            provider.override(providers.Factory(object))

    def test_provide_not_implemented(self):
        provider = providers.AbstractCoroutine(_example)

        with self.assertRaises(NotImplementedError):
            provider._provide((1, 2, 3, 4), dict())

    def test_repr(self):
        provider = providers.AbstractCoroutine(_example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'AbstractCoroutine({0}) at {1}>'.format(
                             repr(_example),
                             hex(id(provider))))


class CoroutineDelegateTests(unittest.TestCase):

    def setUp(self):
        self.delegated = providers.Coroutine(_example)
        self.delegate = providers.CoroutineDelegate(self.delegated)

    def test_is_delegate(self):
        self.assertIsInstance(self.delegate, providers.Delegate)

    def test_init_with_not_callable(self):
        self.assertRaises(errors.Error,
                          providers.CoroutineDelegate,
                          providers.Object(object()))
