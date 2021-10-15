"""Dependency injector factory providers unit tests."""

import sys

import unittest

from dependency_injector import (
    providers,
    errors,
)
from pytest import raises


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
        assert providers.is_provider(providers.Factory(Example)) is True

    def test_init_with_not_callable(self):
        with raises(errors.Error):
            providers.Factory(123)

    def test_init_optional_provides(self):
        provider = providers.Factory()
        provider.set_provides(object)
        assert provider.provides is object
        assert isinstance(provider(), object)

    def test_set_provides_returns_self(self):
        provider = providers.Factory()
        assert provider.set_provides(object) is provider

    def test_init_with_valid_provided_type(self):
        class ExampleProvider(providers.Factory):
            provided_type = Example

        example_provider = ExampleProvider(Example, 1, 2)

        assert isinstance(example_provider(), Example)

    def test_init_with_valid_provided_subtype(self):
        class ExampleProvider(providers.Factory):
            provided_type = Example

        class NewExampe(Example):
            pass

        example_provider = ExampleProvider(NewExampe, 1, 2)

        assert isinstance(example_provider(), NewExampe)

    def test_init_with_invalid_provided_type(self):
        class ExampleProvider(providers.Factory):
            provided_type = Example

        with raises(errors.Error):
            ExampleProvider(list)

    def test_provided_instance_provider(self):
        provider = providers.Factory(Example)
        assert isinstance(provider.provided, providers.ProvidedInstance)

    def test_call(self):
        provider = providers.Factory(Example)

        instance1 = provider()
        instance2 = provider()

        assert instance1 is not instance2
        assert isinstance(instance1, Example)
        assert isinstance(instance2, Example)

    def test_call_with_init_positional_args(self):
        provider = providers.Factory(Example, "i1", "i2")

        instance1 = provider()
        instance2 = provider()

        assert instance1.init_arg1 == "i1"
        assert instance1.init_arg2 == "i2"

        assert instance2.init_arg1 == "i1"
        assert instance2.init_arg2 == "i2"

        assert instance1 is not instance2
        assert isinstance(instance1, Example)
        assert isinstance(instance2, Example)

    def test_call_with_init_keyword_args(self):
        provider = providers.Factory(Example, init_arg1="i1", init_arg2="i2")

        instance1 = provider()
        instance2 = provider()

        assert instance1.init_arg1 == "i1"
        assert instance1.init_arg2 == "i2"

        assert instance2.init_arg1 == "i1"
        assert instance2.init_arg2 == "i2"

        assert instance1 is not instance2
        assert isinstance(instance1, Example)
        assert isinstance(instance2, Example)

    def test_call_with_init_positional_and_keyword_args(self):
        provider = providers.Factory(Example, "i1", init_arg2="i2")

        instance1 = provider()
        instance2 = provider()

        assert instance1.init_arg1 == "i1"
        assert instance1.init_arg2 == "i2"

        assert instance2.init_arg1 == "i1"
        assert instance2.init_arg2 == "i2"

        assert instance1 is not instance2
        assert isinstance(instance1, Example)
        assert isinstance(instance2, Example)

    def test_call_with_attributes(self):
        provider = providers.Factory(Example)
        provider.add_attributes(attribute1="a1", attribute2="a2")

        instance1 = provider()
        instance2 = provider()

        assert instance1.attribute1 == "a1"
        assert instance1.attribute2 == "a2"

        assert instance2.attribute1 == "a1"
        assert instance2.attribute2 == "a2"

        assert instance1 is not instance2
        assert isinstance(instance1, Example)
        assert isinstance(instance2, Example)

    def test_call_with_context_args(self):
        provider = providers.Factory(Example, 11, 22)

        instance = provider(33, 44)

        assert instance.init_arg1 == 11
        assert instance.init_arg2 == 22
        assert instance.init_arg3 == 33
        assert instance.init_arg4 == 44

    def test_call_with_context_kwargs(self):
        provider = providers.Factory(Example, init_arg1=1)

        instance1 = provider(init_arg2=22)
        assert instance1.init_arg1 == 1
        assert instance1.init_arg2 == 22

        instance2 = provider(init_arg1=11, init_arg2=22)
        assert instance2.init_arg1 == 11
        assert instance2.init_arg2 == 22

    def test_call_with_context_args_and_kwargs(self):
        provider = providers.Factory(Example, 11)

        instance = provider(22, init_arg3=33, init_arg4=44)

        assert instance.init_arg1 == 11
        assert instance.init_arg2 == 22
        assert instance.init_arg3 == 33
        assert instance.init_arg4 == 44

    def test_call_with_deep_context_kwargs(self):
        """`Factory` providers deep init injections example."""
        class Regularizer:
            def __init__(self, alpha):
                self.alpha = alpha

        class Loss:
            def __init__(self, regularizer):
                self.regularizer = regularizer

        class ClassificationTask:
            def __init__(self, loss):
                self.loss = loss

        class Algorithm:
            def __init__(self, task):
                self.task = task

        algorithm_factory = providers.Factory(
            Algorithm,
            task=providers.Factory(
                ClassificationTask,
                loss=providers.Factory(
                    Loss,
                    regularizer=providers.Factory(
                        Regularizer,
                    ),
                ),
            ),
        )

        algorithm_1 = algorithm_factory(task__loss__regularizer__alpha=0.5)
        algorithm_2 = algorithm_factory(task__loss__regularizer__alpha=0.7)
        algorithm_3 = algorithm_factory(task__loss__regularizer=Regularizer(alpha=0.8))

        assert algorithm_1.task.loss.regularizer.alpha == 0.5
        assert algorithm_2.task.loss.regularizer.alpha == 0.7
        assert algorithm_3.task.loss.regularizer.alpha == 0.8

    def test_fluent_interface(self):
        provider = providers.Factory(Example) \
            .add_args(1, 2) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .add_attributes(attribute1=5, attribute2=6)

        instance = provider()

        assert instance.init_arg1 == 1
        assert instance.init_arg2 == 2
        assert instance.init_arg3 == 3
        assert instance.init_arg4 == 4
        assert instance.attribute1 == 5
        assert instance.attribute2 == 6

    def test_set_args(self):
        provider = providers.Factory(Example) \
            .add_args(1, 2) \
            .set_args(3, 4)
        assert provider.args == (3, 4)

    def test_set_kwargs(self):
        provider = providers.Factory(Example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .set_kwargs(init_arg3=4, init_arg4=5)
        assert provider.kwargs == dict(init_arg3=4, init_arg4=5)

    def test_set_attributes(self):
        provider = providers.Factory(Example) \
            .add_attributes(attribute1=5, attribute2=6) \
            .set_attributes(attribute1=6, attribute2=7)
        assert provider.attributes == dict(attribute1=6, attribute2=7)

    def test_clear_args(self):
        provider = providers.Factory(Example) \
            .add_args(1, 2) \
            .clear_args()
        assert provider.args == tuple()

    def test_clear_kwargs(self):
        provider = providers.Factory(Example) \
            .add_kwargs(init_arg3=3, init_arg4=4) \
            .clear_kwargs()
        assert provider.kwargs == dict()

    def test_clear_attributes(self):
        provider = providers.Factory(Example) \
            .add_attributes(attribute1=5, attribute2=6) \
            .clear_attributes()
        assert provider.attributes == dict()

    def test_call_overridden(self):
        provider = providers.Factory(Example)
        overriding_provider1 = providers.Factory(dict)
        overriding_provider2 = providers.Factory(list)

        provider.override(overriding_provider1)
        provider.override(overriding_provider2)

        instance1 = provider()
        instance2 = provider()

        assert instance1 is not instance2
        assert isinstance(instance1, list)
        assert isinstance(instance2, list)

    def test_deepcopy(self):
        provider = providers.Factory(Example)

        provider_copy = providers.deepcopy(provider)

        assert provider is not provider_copy
        assert provider.cls is provider_copy.cls
        assert isinstance(provider, providers.Factory)

    def test_deepcopy_from_memo(self):
        provider = providers.Factory(Example)
        provider_copy_memo = providers.Factory(Example)

        provider_copy = providers.deepcopy(provider, memo={id(provider): provider_copy_memo})

        assert provider_copy is provider_copy_memo

    def test_deepcopy_args(self):
        provider = providers.Factory(Example)
        dependent_provider1 = providers.Factory(list)
        dependent_provider2 = providers.Factory(dict)

        provider.add_args(dependent_provider1, dependent_provider2)

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.args[0]
        dependent_provider_copy2 = provider_copy.args[1]

        assert provider.args != provider_copy.args

        assert dependent_provider1.cls is dependent_provider_copy1.cls
        assert dependent_provider1 is not dependent_provider_copy1

        assert dependent_provider2.cls is dependent_provider_copy2.cls
        assert dependent_provider2 is not dependent_provider_copy2

    def test_deepcopy_kwargs(self):
        provider = providers.Factory(Example)
        dependent_provider1 = providers.Factory(list)
        dependent_provider2 = providers.Factory(dict)

        provider.add_kwargs(a1=dependent_provider1, a2=dependent_provider2)

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.kwargs["a1"]
        dependent_provider_copy2 = provider_copy.kwargs["a2"]

        assert provider.kwargs != provider_copy.kwargs

        assert dependent_provider1.cls is dependent_provider_copy1.cls
        assert dependent_provider1 is not dependent_provider_copy1

        assert dependent_provider2.cls is dependent_provider_copy2.cls
        assert dependent_provider2 is not dependent_provider_copy2

    def test_deepcopy_attributes(self):
        provider = providers.Factory(Example)
        dependent_provider1 = providers.Factory(list)
        dependent_provider2 = providers.Factory(dict)

        provider.add_attributes(a1=dependent_provider1, a2=dependent_provider2)

        provider_copy = providers.deepcopy(provider)
        dependent_provider_copy1 = provider_copy.attributes["a1"]
        dependent_provider_copy2 = provider_copy.attributes["a2"]

        assert provider.attributes != provider_copy.attributes

        assert dependent_provider1.cls is dependent_provider_copy1.cls
        assert dependent_provider1 is not dependent_provider_copy1

        assert dependent_provider2.cls is dependent_provider_copy2.cls
        assert dependent_provider2 is not dependent_provider_copy2

    def test_deepcopy_overridden(self):
        provider = providers.Factory(Example)
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        assert provider is not provider_copy
        assert provider.cls is provider_copy.cls
        assert isinstance(provider, providers.Factory)

        assert object_provider is not object_provider_copy
        assert isinstance(object_provider_copy, providers.Object)

    def test_deepcopy_with_sys_streams(self):
        provider = providers.Factory(Example)
        provider.add_args(sys.stdin)
        provider.add_kwargs(a2=sys.stdout)
        provider.add_attributes(a3=sys.stderr)

        provider_copy = providers.deepcopy(provider)

        assert provider is not provider_copy
        assert isinstance(provider_copy, providers.Factory)
        assert provider.args[0] is sys.stdin
        assert provider.kwargs["a2"] is sys.stdout
        assert provider.attributes["a3"] is sys.stderr

    def test_repr(self):
        provider = providers.Factory(Example)
        assert repr(provider) == (
            "<dependency_injector.providers."
            "Factory({0}) at {1}>".format(repr(Example), hex(id(provider)))
        )


class DelegatedFactoryTests(unittest.TestCase):

    def test_inheritance(self):
        assert isinstance(providers.DelegatedFactory(object),
                              providers.Factory)

    def test_is_provider(self):
        assert providers.is_provider(providers.DelegatedFactory(object)) is True

    def test_is_delegated_provider(self):
        assert providers.is_delegated(providers.DelegatedFactory(object)) is True

    def test_repr(self):
        provider = providers.DelegatedFactory(Example)
        assert repr(provider) == (
            "<dependency_injector.providers."
            "DelegatedFactory({0}) at {1}>".format(repr(Example), hex(id(provider)))
        )


class AbstractFactoryTests(unittest.TestCase):

    def test_inheritance(self):
        assert isinstance(providers.AbstractFactory(Example),
                              providers.Factory)

    def test_call_overridden_by_factory(self):
        provider = providers.AbstractFactory(object)
        provider.override(providers.Factory(Example))

        assert isinstance(provider(), Example)

    def test_call_overridden_by_delegated_factory(self):
        provider = providers.AbstractFactory(object)
        provider.override(providers.DelegatedFactory(Example))

        assert isinstance(provider(), Example)

    def test_call_not_overridden(self):
        provider = providers.AbstractFactory(object)
        with raises(errors.Error):
            provider()

    def test_override_by_not_factory(self):
        provider = providers.AbstractFactory(object)
        with raises(errors.Error):
            provider.override(providers.Callable(object))

    def test_provide_not_implemented(self):
        provider = providers.AbstractFactory(Example)
        with raises(NotImplementedError):
            provider._provide(tuple(), dict())

    def test_repr(self):
        provider = providers.AbstractFactory(Example)
        assert repr(provider) == (
            "<dependency_injector.providers."
            "AbstractFactory({0}) at {1}>".format(repr(Example), hex(id(provider)))
        )


class FactoryDelegateTests(unittest.TestCase):

    def setUp(self):
        self.delegated = providers.Factory(object)
        self.delegate = providers.FactoryDelegate(self.delegated)

    def test_is_delegate(self):
        assert isinstance(self.delegate, providers.Delegate)

    def test_init_with_not_factory(self):
        with raises(errors.Error):
            providers.FactoryDelegate(providers.Object(object()))


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
            example_b=self.example_b_factory,
        )

    def test_is_provider(self):
        assert providers.is_provider(self.factory_aggregate) is True

    def test_is_delegated_provider(self):
        assert providers.is_delegated(self.factory_aggregate) is True

    def test_init_with_non_string_keys(self):
        factory = providers.FactoryAggregate({
            self.ExampleA: self.example_a_factory,
            self.ExampleB: self.example_b_factory,
        })

        object_a = factory(self.ExampleA, 1, 2, init_arg3=3, init_arg4=4)
        object_b = factory(self.ExampleB, 11, 22, init_arg3=33, init_arg4=44)

        assert isinstance(object_a, self.ExampleA)
        assert object_a.init_arg1 == 1
        assert object_a.init_arg2 == 2
        assert object_a.init_arg3 == 3
        assert object_a.init_arg4 == 4

        assert isinstance(object_b, self.ExampleB)
        assert object_b.init_arg1 == 11
        assert object_b.init_arg2 == 22
        assert object_b.init_arg3 == 33
        assert object_b.init_arg4 == 44

        assert factory.factories == {
            self.ExampleA: self.example_a_factory,
            self.ExampleB: self.example_b_factory,
        }

    def test_init_with_not_a_factory(self):
        with raises(errors.Error):
            providers.FactoryAggregate(
                example_a=providers.Factory(self.ExampleA),
                example_b=object())

    def test_init_optional_factories(self):
        provider = providers.FactoryAggregate()
        provider.set_factories(
            example_a=self.example_a_factory,
            example_b=self.example_b_factory,
        )
        assert provider.factories == {
            "example_a": self.example_a_factory,
            "example_b": self.example_b_factory,
        }
        assert isinstance(provider("example_a"), self.ExampleA)
        assert isinstance(provider("example_b"), self.ExampleB)

    def test_set_factories_with_non_string_keys(self):
        factory = providers.FactoryAggregate()
        factory.set_factories({
            self.ExampleA: self.example_a_factory,
            self.ExampleB: self.example_b_factory,
        })

        object_a = factory(self.ExampleA, 1, 2, init_arg3=3, init_arg4=4)
        object_b = factory(self.ExampleB, 11, 22, init_arg3=33, init_arg4=44)

        assert isinstance(object_a, self.ExampleA)
        assert object_a.init_arg1 == 1
        assert object_a.init_arg2 == 2
        assert object_a.init_arg3 == 3
        assert object_a.init_arg4 == 4

        assert isinstance(object_b, self.ExampleB)
        assert object_b.init_arg1 == 11
        assert object_b.init_arg2 == 22
        assert object_b.init_arg3 == 33
        assert object_b.init_arg4 == 44

        assert factory.factories == {
            self.ExampleA: self.example_a_factory,
            self.ExampleB: self.example_b_factory,
        }

    def test_set_factories_returns_self(self):
        provider = providers.FactoryAggregate()
        assert provider.set_factories(example_a=self.example_a_factory) is provider

    def test_call(self):
        object_a = self.factory_aggregate("example_a",
                                          1, 2, init_arg3=3, init_arg4=4)
        object_b = self.factory_aggregate("example_b",
                                          11, 22, init_arg3=33, init_arg4=44)

        assert isinstance(object_a, self.ExampleA)
        assert object_a.init_arg1 == 1
        assert object_a.init_arg2 == 2
        assert object_a.init_arg3 == 3
        assert object_a.init_arg4 == 4

        assert isinstance(object_b, self.ExampleB)
        assert object_b.init_arg1 == 11
        assert object_b.init_arg2 == 22
        assert object_b.init_arg3 == 33
        assert object_b.init_arg4 == 44

    def test_call_factory_name_as_kwarg(self):
        object_a = self.factory_aggregate(
            factory_name="example_a",
            init_arg1=1,
            init_arg2=2,
            init_arg3=3,
            init_arg4=4,
        )
        assert isinstance(object_a, self.ExampleA)
        assert object_a.init_arg1 == 1
        assert object_a.init_arg2 == 2
        assert object_a.init_arg3 == 3
        assert object_a.init_arg4 == 4

    def test_call_no_factory_name(self):
        with raises(TypeError):
            self.factory_aggregate()

    def test_call_no_such_provider(self):
        with raises(errors.NoSuchProviderError):
            self.factory_aggregate("unknown")

    def test_overridden(self):
        with raises(errors.Error):
            self.factory_aggregate.override(providers.Object(object()))

    def test_getattr(self):
        assert self.factory_aggregate.example_a is self.example_a_factory
        assert self.factory_aggregate.example_b is self.example_b_factory

    def test_getattr_no_such_provider(self):
        with raises(errors.NoSuchProviderError):
            self.factory_aggregate.unknown

    def test_factories(self):
        assert self.factory_aggregate.factories == dict(
            example_a=self.example_a_factory,
            example_b=self.example_b_factory,
        )

    def test_deepcopy(self):
        provider_copy = providers.deepcopy(self.factory_aggregate)

        assert self.factory_aggregate is not provider_copy
        assert isinstance(provider_copy, type(self.factory_aggregate))

        assert self.factory_aggregate.example_a is not provider_copy.example_a
        assert isinstance(self.factory_aggregate.example_a, type(provider_copy.example_a))
        assert self.factory_aggregate.example_a.cls is provider_copy.example_a.cls

        assert self.factory_aggregate.example_b is not provider_copy.example_b
        assert isinstance(self.factory_aggregate.example_b, type(provider_copy.example_b))
        assert self.factory_aggregate.example_b.cls is provider_copy.example_b.cls

    def test_deepcopy_with_non_string_keys(self):
        factory_aggregate = providers.FactoryAggregate({
            self.ExampleA: self.example_a_factory,
            self.ExampleB: self.example_b_factory,
        })
        provider_copy = providers.deepcopy(factory_aggregate)

        assert factory_aggregate is not provider_copy
        assert isinstance(provider_copy, type(factory_aggregate))

        assert factory_aggregate.factories[self.ExampleA] is not provider_copy.factories[self.ExampleA]
        assert isinstance(factory_aggregate.factories[self.ExampleA], type(provider_copy.factories[self.ExampleA]))
        assert factory_aggregate.factories[self.ExampleA].cls is provider_copy.factories[self.ExampleA].cls

        assert factory_aggregate.factories[self.ExampleB] is not provider_copy.factories[self.ExampleB]
        assert isinstance(factory_aggregate.factories[self.ExampleB], type(provider_copy.factories[self.ExampleB]))
        assert factory_aggregate.factories[self.ExampleB].cls is provider_copy.factories[self.ExampleB].cls

    def test_repr(self):
        assert repr(self.factory_aggregate) == (
            "<dependency_injector.providers."
            "FactoryAggregate({0}) at {1}>".format(
                repr(self.factory_aggregate.factories),
                hex(id(self.factory_aggregate)),
            )
        )
