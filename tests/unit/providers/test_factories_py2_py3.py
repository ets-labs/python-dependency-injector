"""Dependency injector factory providers unit tests."""

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


class FactoryTests(unittest.TestCase):

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(providers.Factory(Example)))

    def test_init_with_callable(self):
        self.assertTrue(providers.Factory(credits))

    def test_init_with_not_callable(self):
        self.assertRaises(errors.Error, providers.Factory, 123)

    def test_init_with_valid_provided_type(self):
        class ExampleProvider(providers.Factory):
            provided_type = Example

        example_provider = ExampleProvider(Example, 1, 2)

        self.assertIsInstance(example_provider(), Example)

    def test_init_with_valid_provided_subtype(self):
        class ExampleProvider(providers.Factory):
            provided_type = Example

        class NewExampe(Example):
            pass

        example_provider = ExampleProvider(NewExampe, 1, 2)

        self.assertIsInstance(example_provider(), NewExampe)

    def test_init_with_invalid_provided_type(self):
        class ExampleProvider(providers.Factory):
            provided_type = Example

        with self.assertRaises(errors.Error):
            ExampleProvider(list)

    def test_call(self):
        provider = providers.Factory(Example)

        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_args(self):
        provider = providers.Factory(Example, 'i1', 'i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_keyword_args(self):
        provider = providers.Factory(Example, init_arg1='i1', init_arg2='i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_init_positional_and_keyword_args(self):
        provider = providers.Factory(Example, 'i1', init_arg2='i2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.init_arg1, 'i1')
        self.assertEqual(instance1.init_arg2, 'i2')

        self.assertEqual(instance2.init_arg1, 'i1')
        self.assertEqual(instance2.init_arg2, 'i2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_attributes(self):
        provider = providers.Factory(Example)
        provider.add_attributes(attribute1='a1', attribute2='a2')

        instance1 = provider()
        instance2 = provider()

        self.assertEqual(instance1.attribute1, 'a1')
        self.assertEqual(instance1.attribute2, 'a2')

        self.assertEqual(instance2.attribute1, 'a1')
        self.assertEqual(instance2.attribute2, 'a2')

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, Example)
        self.assertIsInstance(instance2, Example)

    def test_call_with_context_args(self):
        provider = providers.Factory(Example, 11, 22)

        instance = provider(33, 44)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)
        self.assertEqual(instance.init_arg3, 33)
        self.assertEqual(instance.init_arg4, 44)

    def test_call_with_context_kwargs(self):
        provider = providers.Factory(Example, init_arg1=1)

        instance1 = provider(init_arg2=22)
        self.assertEqual(instance1.init_arg1, 1)
        self.assertEqual(instance1.init_arg2, 22)

        instance2 = provider(init_arg1=11, init_arg2=22)
        self.assertEqual(instance2.init_arg1, 11)
        self.assertEqual(instance2.init_arg2, 22)

    def test_call_with_context_args_and_kwargs(self):
        provider = providers.Factory(Example, 11)

        instance = provider(22, init_arg3=33, init_arg4=44)

        self.assertEqual(instance.init_arg1, 11)
        self.assertEqual(instance.init_arg2, 22)
        self.assertEqual(instance.init_arg3, 33)
        self.assertEqual(instance.init_arg4, 44)

    def test_fluent_interface(self):
        provider = providers.Factory(Example) \
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
        provider = providers.Factory(Example) \
            .add_args(1, 2) \
            .set_args(3, 4)
        self.assertEqual(provider.args, tuple([3, 4]))

    def test_set_kwargs(self):
        provider = providers.Factory(Example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .set_kwargs(init_arg3=4, init_arg4=5)
        self.assertEqual(provider.kwargs, dict(init_arg3=4, init_arg4=5))

    def test_set_attributes(self):
        provider = providers.Factory(Example) \
            .add_attributes(attribute1=5, attribute2=6) \
            .set_attributes(attribute1=6, attribute2=7)
        self.assertEqual(provider.attributes, dict(attribute1=6, attribute2=7))

    def test_clear_args(self):
        provider = providers.Factory(Example) \
            .add_args(1, 2) \
            .clear_args()
        self.assertEqual(provider.args, tuple())

    def test_clear_kwargs(self):
        provider = providers.Factory(Example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .clear_kwargs()
        self.assertEqual(provider.kwargs, dict())

    def test_clear_attributes(self):
        provider = providers.Factory(Example) \
            .add_attributes(attribute1=5, attribute2=6) \
            .clear_attributes()
        self.assertEqual(provider.attributes, dict())

    def test_call_overridden(self):
        provider = providers.Factory(Example)
        overriding_provider1 = providers.Factory(dict)
        overriding_provider2 = providers.Factory(list)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        self.assertIsNot(instance1, instance2)
        self.assertIsInstance(instance1, list)
        self.assertIsInstance(instance2, list)

    def test_deepcopy(self):
        provider = providers.Factory(Example)

        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIs(provider.cls, provider_copy.cls)
        self.assertIsInstance(provider, providers.Factory)

    def test_deepcopy_from_memo(self):
        provider = providers.Factory(Example)
        provider_copy_memo = providers.Factory(Example)

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_args(self):
        provider = providers.Factory(Example)
        dependent_provider1 = providers.Factory(list)
        dependent_provider2 = providers.Factory(dict)

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
        provider = providers.Factory(Example)
        dependent_provider1 = providers.Factory(list)
        dependent_provider2 = providers.Factory(dict)

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
        provider = providers.Factory(Example)
        dependent_provider1 = providers.Factory(list)
        dependent_provider2 = providers.Factory(dict)

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
        provider = providers.Factory(Example)
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIs(provider.cls, provider_copy.cls)
        self.assertIsInstance(provider, providers.Factory)

        self.assertIsNot(object_provider, object_provider_copy)
        self.assertIsInstance(object_provider_copy, providers.Object)

    def test_repr(self):
        provider = providers.Factory(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'Factory({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class DelegatedFactoryTests(unittest.TestCase):

    def test_inheritance(self):
        self.assertIsInstance(providers.DelegatedFactory(object),
                              providers.Factory)

    def test_is_provider(self):
        self.assertTrue(
            providers.is_provider(providers.DelegatedFactory(object)))

    def test_is_delegated_provider(self):
        self.assertTrue(
            providers.is_delegated(providers.DelegatedFactory(object)))

    def test_repr(self):
        provider = providers.DelegatedFactory(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'DelegatedFactory({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class AbstractFactoryTests(unittest.TestCase):

    def test_inheritance(self):
        self.assertIsInstance(providers.AbstractFactory(Example),
                              providers.Factory)

    def test_call_overridden_by_factory(self):
        provider = providers.AbstractFactory(object)
        provider.override(providers.Factory(Example))

        self.assertIsInstance(provider(), Example)

    def test_call_overridden_by_delegated_factory(self):
        provider = providers.AbstractFactory(object)
        provider.override(providers.DelegatedFactory(Example))

        self.assertIsInstance(provider(), Example)

    def test_call_not_overridden(self):
        provider = providers.AbstractFactory(object)

        with self.assertRaises(errors.Error):
            provider()

    def test_override_by_not_factory(self):
        provider = providers.AbstractFactory(object)

        with self.assertRaises(errors.Error):
            provider.override(providers.Callable(object))

    def test_provide_not_implemented(self):
        provider = providers.AbstractFactory(Example)

        with self.assertRaises(NotImplementedError):
            provider._provide(tuple(), dict())

    def test_repr(self):
        provider = providers.AbstractFactory(Example)

        self.assertEqual(repr(provider),
                         '<dependency_injector.providers.'
                         'AbstractFactory({0}) at {1}>'.format(
                             repr(Example),
                             hex(id(provider))))


class FactoryDelegateTests(unittest.TestCase):

    def setUp(self):
        self.delegated = providers.Factory(object)
        self.delegate = providers.FactoryDelegate(self.delegated)

    def test_is_delegate(self):
        self.assertIsInstance(self.delegate, providers.Delegate)

    def test_init_with_not_factory(self):
        self.assertRaises(errors.Error,
                          providers.FactoryDelegate,
                          providers.Object(object()))


class FactoryAggregateTests(unittest.TestCase):

    class ExampleA(Example):
        pass

    class ExampleB(Example):
        pass

    def setUp(self):
        self.example_a_factory = providers.Factory(self.ExampleA)
        self.example_b_factory = providers.Factory(self.ExampleB)
        self.factory_aggregate = providers.FactoryAggregate(
            example_a=self.example_a_factory,
            example_b=self.example_b_factory)

    def test_is_provider(self):
        self.assertTrue(providers.is_provider(self.factory_aggregate))

    def test_is_delegated_provider(self):
        self.assertTrue(providers.is_delegated(self.factory_aggregate))

    def test_init_with_not_a_factory(self):
        with self.assertRaises(errors.Error):
            providers.FactoryAggregate(
                example_a=providers.Factory(self.ExampleA),
                example_b=object())

    def test_call(self):
        object_a = self.factory_aggregate('example_a',
                                          1, 2, init_arg3=3, init_arg4=4)
        object_b = self.factory_aggregate('example_b',
                                          11, 22, init_arg3=33, init_arg4=44)

        self.assertIsInstance(object_a, self.ExampleA)
        self.assertEqual(object_a.init_arg1, 1)
        self.assertEqual(object_a.init_arg2, 2)
        self.assertEqual(object_a.init_arg3, 3)
        self.assertEqual(object_a.init_arg4, 4)

        self.assertIsInstance(object_b, self.ExampleB)
        self.assertEqual(object_b.init_arg1, 11)
        self.assertEqual(object_b.init_arg2, 22)
        self.assertEqual(object_b.init_arg3, 33)
        self.assertEqual(object_b.init_arg4, 44)

    def test_call_no_such_provider(self):
        with self.assertRaises(errors.NoSuchProviderError):
            self.factory_aggregate('unknown')

    def test_overridden(self):
        with self.assertRaises(errors.Error):
            self.factory_aggregate.override(providers.Object(object()))

    def test_getattr(self):
        self.assertIs(self.factory_aggregate.example_a, self.example_a_factory)
        self.assertIs(self.factory_aggregate.example_b, self.example_b_factory)

    def test_getattr_no_such_provider(self):
        with self.assertRaises(errors.NoSuchProviderError):
            self.factory_aggregate.unknown

    def test_factories(self):
        self.assertDictEqual(self.factory_aggregate.factories,
                             dict(example_a=self.example_a_factory,
                                  example_b=self.example_b_factory))

    def test_repr(self):
        self.assertEqual(repr(self.factory_aggregate),
                         '<dependency_injector.providers.'
                         'FactoryAggregate({0}) at {1}>'.format(
                             repr(self.factory_aggregate.factories),
                             hex(id(self.factory_aggregate))))
