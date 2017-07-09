"""Dependency injector singleton providers unit tests."""

import unittest2 as unittest

from dependency_injector import (
    providers,
    errors,
)


class Example(object):

    def __init__(self, init_arg1=None, init_arg2=None, init_arg3=None,
                 init_arg4=None):
        self.init_arg1 = init_arg1
        self.init_arg2 = init_arg2
        self.init_arg3 = init_arg3
        self.init_arg4 = init_arg4

        self.attribute1 = None
        self.attribute2 = None


class _BaseSingletonTestCase(object):

    singleton_cls = None

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.singleton_cls(Example)))

    def test_init_with_callable(self):
        self.assertTrue(self.singleton_cls(credits))

    def test_init_with_not_callable(self):
        self.assertRaises(errors.Error, self.singleton_cls, 123)

    def test_init_with_valid_provided_type(self):
        class ExampleProvider(self.singleton_cls):
            provided_type = Example

        example_provider = ExampleProvider(Example, 1, 2)

        self.assertIsInstance(example_provider(), Example)

    def test_init_with_valid_provided_subtype(self):
        class ExampleProvider(self.singleton_cls):
            provided_type = Example

        class NewExampe(Example):
            pass

        example_provider = ExampleProvider(NewExampe, 1, 2)

        self.assertIsInstance(example_provider(), NewExampe)

    def test_init_with_invalid_provided_type(self):
        class ExampleProvider(self.singleton_cls):
            provided_type = Example

        with self.assertRaises(errors.Error):
            ExampleProvider(list)

    def test_call(self):
        provider = self.singleton_cls(Example)

        instance1 = provider()
        instance2 = provider()

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_args(self):
        provider = self.singleton_cls(Example, 'i1', 'i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_keyword_args(self):
        provider = self.singleton_cls(Example, init_arg1='i1', init_arg2='i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_and_keyword_args(self):
        provider = self.singleton_cls(Example, 'i1', init_arg2='i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_attributes(self):
        provider = self.singleton_cls(Example)
        provider.add_attributes(attribute1='a1', attribute2='a2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.attribute1, 'a1')
        self.assertEqual(instance1.attribute2, 'a2')

        self.assertEqual(instance2.attribute1, 'a1')
        self.assertEqual(instance2.attribute2, 'a2')

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_context_args(self):
        provider = self.singleton_cls(Example)

        instance = provider(11, 22)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)

    def test_call_with_context_kwargs(self):
        provider = self.singleton_cls(Example, init_arg1=1)

        instance1 = provider(init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

        # Instance is created earlier
        instance1 = provider(init_arg1=11, init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

    def test_call_with_context_args_and_kwargs(self):
        provider = self.singleton_cls(Example, 11)

        instance = provider(22, init_arg3=33, init_arg4=44)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)
        self.assertEqual(instance.init_arg3, 33)
        self.assertEqual(instance.init_arg4, 44)

    def test_fluent_interface(self):
        provider = self.singleton_cls(Example) \
            .add_args(1, 2) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .add_attributes(attribute1=5, attribute2=6)

        instance = provider()

        self.assertEqual(instance.init_arg1, 1)
        self.assertEqual(instance.init_arg2, 2)
        self.assertEqual(instance.init_arg3, 3)
        self.assertEqual(instance.init_arg4, 4)
        self.assertEqual(instance.attribute1, 5)
        self.assertEqual(instance.attribute2, 6)

    def test_set_args(self):
        provider = self.singleton_cls(Example) \
            .add_args(1, 2) \
            .set_args(3, 4)
        self.assertEqual(provider.args, tuple([3, 4]))

    def test_set_kwargs(self):
        provider = self.singleton_cls(Example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .set_kwargs(init_arg3=4, init_arg4=5)
        self.assertEqual(provider.kwargs, dict(init_arg3=4, init_arg4=5))

    def test_set_attributes(self):
        provider = self.singleton_cls(Example) \
            .add_attributes(attribute1=5, attribute2=6) \
            .set_attributes(attribute1=6, attribute2=7)
        self.assertEqual(provider.attributes, dict(attribute1=6, attribute2=7))

    def test_clear_args(self):
        provider = self.singleton_cls(Example) \
            .add_args(1, 2) \
            .clear_args()
        self.assertEqual(provider.args, tuple())

    def test_clear_kwargs(self):
        provider = self.singleton_cls(Example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .clear_kwargs()
        self.assertEqual(provider.kwargs, dict())

    def test_clear_attributes(self):
        provider = self.singleton_cls(Example) \
            .add_attributes(attribute1=5, attribute2=6) \
            .clear_attributes()
        self.assertEqual(provider.attributes, dict())

    def test_call_overridden(self):
        provider = self.singleton_cls(Example)
        overriding_provider1 = self.singleton_cls(dict)
        overriding_provider2 = self.singleton_cls(list)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance1, list)
        self.assertIsInstance(instance2, list)

    def test_deepcopy(self):
        provider = self.singleton_cls(Example)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIs(provider.cls, provider_copy.cls)
        self.assertIsInstance(provider, self.singleton_cls)

    def test_deepcopy_from_memo(self):
        provider = self.singleton_cls(Example)
        provider_copy_memo = self.singleton_cls(Example)

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_args(self):
        provider = self.singleton_cls(Example)
        dependent_provider1 = self.singleton_cls(list)
        dependent_provider2 = self.singleton_cls(dict)

        provider.add_args(dependent_provider1, dependent_provider2)

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.args[0]
        dependent_provider_copy2 = provider_copy.args[1]

        self.assertNotEqual(provider.args, provider_copy.args)

        self.assertIs(dependent_provider1.cls, dependent_provider_copy1.cls)
        self.assertIsNot(dependent_provider1, dependent_provider_copy1)

        self.assertIs(dependent_provider2.cls, dependent_provider_copy2.cls)
        self.assertIsNot(dependent_provider2, dependent_provider_copy2)

    def test_deepcopy_kwargs(self):
        provider = self.singleton_cls(Example)
        dependent_provider1 = self.singleton_cls(list)
        dependent_provider2 = self.singleton_cls(dict)

        provider.add_kwargs(a1=dependent_provider1, a2=dependent_provider2)

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.kwargs['a1']
        dependent_provider_copy2 = provider_copy.kwargs['a2']

        self.assertNotEqual(provider.kwargs, provider_copy.kwargs)

        self.assertIs(dependent_provider1.cls, dependent_provider_copy1.cls)
        self.assertIsNot(dependent_provider1, dependent_provider_copy1)

        self.assertIs(dependent_provider2.cls, dependent_provider_copy2.cls)
        self.assertIsNot(dependent_provider2, dependent_provider_copy2)

    def test_deepcopy_attributes(self):
        provider = self.singleton_cls(Example)
        dependent_provider1 = self.singleton_cls(list)
        dependent_provider2 = self.singleton_cls(dict)

        provider.add_attributes(a1=dependent_provider1, a2=dependent_provider2)

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.attributes['a1']
        dependent_provider_copy2 = provider_copy.attributes['a2']

        self.assertNotEqual(provider.attributes, provider_copy.attributes)

        self.assertIs(dependent_provider1.cls, dependent_provider_copy1.cls)
        self.assertIsNot(dependent_provider1, dependent_provider_copy1)

        self.assertIs(dependent_provider2.cls, dependent_provider_copy2.cls)
        self.assertIsNot(dependent_provider2, dependent_provider_copy2)

    def test_deepcopy_overridden(self):
        provider = self.singleton_cls(Example)
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIs(provider.cls, provider_copy.cls)
        self.assertIsInstance(provider, self.singleton_cls)

        self.assertIsNot(object_provider, object_provider_copy)
        self.assertIsInstance(object_provider_copy, providers.Object)

    def test_reset(self):
        provider = self.singleton_cls(object)

        instance1 = provider()
        self.assertIsInstance(instance1, object)

        provider.reset()

        instance2 = provider()
        self.assertIsInstance(instance1, object)

        self.assertIsNot(instance1, instance2)


class SingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.Singleton

    def test_repr(self):
        provider = self.singleton_cls(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'Singleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class DelegatedSingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.DelegatedSingleton

    def test_is_delegated_provider(self):
        provider = self.singleton_cls(object)
        self.assertTrue(providers.is_delegated(provider))

    def test_repr(self):
        provider = self.singleton_cls(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'DelegatedSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class ThreadLocalSingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.ThreadLocalSingleton

    def test_repr(self):
        provider = providers.ThreadLocalSingleton(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'ThreadLocalSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class DelegatedThreadLocalSingletonTests(_BaseSingletonTestCase,
                                         unittest.TestCase):

    singleton_cls = providers.DelegatedThreadLocalSingleton

    def test_is_delegated_provider(self):
        provider = self.singleton_cls(object)
        self.assertTrue(providers.is_delegated(provider))

    def test_repr(self):
        provider = self.singleton_cls(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'DelegatedThreadLocalSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class ThreadSafeSingletonTests(_BaseSingletonTestCase, unittest.TestCase):

    singleton_cls = providers.ThreadSafeSingleton

    def test_repr(self):
        provider = self.singleton_cls(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'ThreadSafeSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class DelegatedThreadSafeSingletonTests(_BaseSingletonTestCase,
                                        unittest.TestCase):

    singleton_cls = providers.DelegatedThreadSafeSingleton

    def test_is_delegated_provider(self):
        provider = self.singleton_cls(object)
        self.assertTrue(providers.is_delegated(provider))

    def test_repr(self):
        provider = self.singleton_cls(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'DelegatedThreadSafeSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class AbstractSingletonTests(unittest.TestCase):

    def test_inheritance(self):
        self.assertIsInstance(providers.AbstractSingleton(Example),
                              providers.BaseSingleton)

    def test_call_overridden_by_singleton(self):
        provider = providers.AbstractSingleton(object)
        provider.override(providers.Singleton(Example))

        self.assertIsInstance(provider(), Example)

    def test_call_overridden_by_delegated_singleton(self):
        provider = providers.AbstractSingleton(object)
        provider.override(providers.DelegatedSingleton(Example))

        self.assertIsInstance(provider(), Example)

    def test_call_not_overridden(self):
        provider = providers.AbstractSingleton(object)

        with self.assertRaises(errors.Error):
            provider()

    def test_reset_overridden(self):
        provider = providers.AbstractSingleton(object)
        provider.override(providers.Singleton(Example))

        instance1 = provider()

        provider.reset()

        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_reset_not_overridden(self):
        provider = providers.AbstractSingleton(object)

        with self.assertRaises(errors.Error):
            provider.reset()

    def test_override_by_not_singleton(self):
        provider = providers.AbstractSingleton(object)

        with self.assertRaises(errors.Error):
            provider.override(providers.Factory(object))

    def test_repr(self):
        provider = providers.AbstractSingleton(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'AbstractSingleton({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class SingletonDelegateTests(unittest.TestCase):

    def setUp(self):
        self.delegated = providers.Singleton(Example)
        self.delegate = providers.SingletonDelegate(self.delegated)

    def test_is_delegate(self):
        self.assertIsInstance(self.delegate, providers.Delegate)

    def test_init_with_not_singleton(self):
        self.assertRaises(errors.Error,
                          providers.SingletonDelegate,
                          providers.Object(object()))
