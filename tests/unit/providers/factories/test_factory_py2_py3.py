"""Factory provider tests."""

import decimal
import sys

from dependency_injector import providers, errors
from pytest import raises, mark

from .common import Example


def test_is_provider():
    assert providers.is_provider(providers.Factory(Example)) is True


def test_init_with_not_callable():
    with raises(errors.Error):
        providers.Factory(123)


def test_init_optional_provides():
    provider = providers.Factory()
    provider.set_provides(object)
    assert provider.provides is object
    assert isinstance(provider(), object)


def test_set_provides_returns_():
    provider = providers.Factory()
    assert provider.set_provides(object) is provider


@mark.parametrize(
    "str_name,cls",
    [
        ("dependency_injector.providers.Factory", providers.Factory),
        ("decimal.Decimal", decimal.Decimal),
        ("list", list),
        (".common.Example", Example),
        ("test_is_provider", test_is_provider),
    ],
)
def test_set_provides_string_imports(str_name, cls):
    assert providers.Factory(str_name).provides is cls


def test_init_with_valid_provided_type():
    class ExampleProvider(providers.Factory):
        provided_type = Example

    example_provider = ExampleProvider(Example, 1, 2)

    assert isinstance(example_provider(), Example)


def test_init_with_valid_provided_subtype():
    class ExampleProvider(providers.Factory):
        provided_type = Example

    class NewExample(Example):
        pass

    example_provider = ExampleProvider(NewExample, 1, 2)
    assert isinstance(example_provider(), NewExample)


def test_init_with_invalid_provided_type():
    class ExampleProvider(providers.Factory):
        provided_type = Example

    with raises(errors.Error):
        ExampleProvider(list)


def test_provided_instance_provider():
    provider = providers.Factory(Example)
    assert isinstance(provider.provided, providers.ProvidedInstance)


def test_call():
    provider = providers.Factory(Example)

    instance1 = provider()
    instance2 = provider()

    assert instance1 is not instance2
    assert isinstance(instance1, Example)
    assert isinstance(instance2, Example)


def test_call_with_init_positional_args():
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


def test_call_with_init_keyword_args():
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


def test_call_with_init_positional_and_keyword_args():
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


def test_call_with_attributes():
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


def test_call_with_context_args():
    provider = providers.Factory(Example, 11, 22)

    instance = provider(33, 44)

    assert instance.init_arg1 == 11
    assert instance.init_arg2 == 22
    assert instance.init_arg3 == 33
    assert instance.init_arg4 == 44


def test_call_with_context_kwargs():
    provider = providers.Factory(Example, init_arg1=1)

    instance1 = provider(init_arg2=22)
    assert instance1.init_arg1 == 1
    assert instance1.init_arg2 == 22

    instance2 = provider(init_arg1=11, init_arg2=22)
    assert instance2.init_arg1 == 11
    assert instance2.init_arg2 == 22


def test_call_with_context_args_and_kwargs():
    provider = providers.Factory(Example, 11)

    instance = provider(22, init_arg3=33, init_arg4=44)

    assert instance.init_arg1 == 11
    assert instance.init_arg2 == 22
    assert instance.init_arg3 == 33
    assert instance.init_arg4 == 44


def test_call_with_deep_context_kwargs():
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


def test_fluent_interface():
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


def test_set_args():
    provider = providers.Factory(Example) \
        .add_args(1, 2) \
        .set_args(3, 4)
    assert provider.args == (3, 4)


def test_set_kwargs():
    provider = providers.Factory(Example) \
        .add_kwargs(init_arg3=3, init_arg4=4) \
        .set_kwargs(init_arg3=4, init_arg4=5)
    assert provider.kwargs == dict(init_arg3=4, init_arg4=5)


def test_set_attributes():
    provider = providers.Factory(Example) \
        .add_attributes(attribute1=5, attribute2=6) \
        .set_attributes(attribute1=6, attribute2=7)
    assert provider.attributes == dict(attribute1=6, attribute2=7)


def test_clear_args():
    provider = providers.Factory(Example) \
        .add_args(1, 2) \
        .clear_args()
    assert provider.args == tuple()


def test_clear_kwargs():
    provider = providers.Factory(Example) \
        .add_kwargs(init_arg3=3, init_arg4=4) \
        .clear_kwargs()
    assert provider.kwargs == dict()


def test_clear_attributes():
    provider = providers.Factory(Example) \
        .add_attributes(attribute1=5, attribute2=6) \
        .clear_attributes()
    assert provider.attributes == dict()


def test_call_overridden():
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


def test_deepcopy():
    provider = providers.Factory(Example)

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert provider.cls is provider_copy.cls
    assert isinstance(provider, providers.Factory)


def test_deepcopy_from_memo():
    provider = providers.Factory(Example)
    provider_copy_memo = providers.Factory(Example)

    provider_copy = providers.deepcopy(provider, memo={id(provider): provider_copy_memo})

    assert provider_copy is provider_copy_memo


def test_deepcopy_args():
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


def test_deepcopy_kwargs():
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


def test_deepcopy_attributes():
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


def test_deepcopy_overridden():
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


def test_deepcopy_with_sys_streams():
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


def test_repr():
    provider = providers.Factory(Example)
    assert repr(provider) == (
        "<dependency_injector.providers."
        "Factory({0}) at {1}>".format(repr(Example), hex(id(provider)))
    )
