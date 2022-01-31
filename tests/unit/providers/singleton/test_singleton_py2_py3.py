"""Singleton provider tests."""
import decimal
import sys

from dependency_injector import providers, errors
from pytest import fixture, raises, mark

from .common import Example


PROVIDER_CLASSES = [
    providers.Singleton,
    providers.DelegatedSingleton,
    providers.ThreadLocalSingleton,
    providers.DelegatedThreadLocalSingleton,
    providers.ThreadSafeSingleton,
    providers.DelegatedThreadSafeSingleton,
]
if sys.version_info >= (3, 5):
    PROVIDER_CLASSES.append(providers.ContextLocalSingleton)


@fixture(params=PROVIDER_CLASSES)
def singleton_cls(request):
    return request.param


@fixture
def provider(singleton_cls):
    return singleton_cls(Example)


def test_is_provider(provider):
    assert providers.is_provider(provider) is True


def test_init_with_not_callable(singleton_cls):
    with raises(errors.Error):
        singleton_cls(123)


def test_init_optional_provides(provider):
    provider.set_provides(object)
    assert provider.provides is object
    assert isinstance(provider(), object)


def test_set_provides_returns_self(provider):
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
    assert providers.Singleton(str_name).provides is cls


def test_init_with_valid_provided_type(singleton_cls):
    class ExampleProvider(singleton_cls):
        provided_type = Example

    example_provider = ExampleProvider(Example, 1, 2)
    assert isinstance(example_provider(), Example)


def test_init_with_valid_provided_subtype(singleton_cls):
    class ExampleProvider(singleton_cls):
        provided_type = Example

    class NewExample(Example):
        pass

    example_provider = ExampleProvider(NewExample, 1, 2)
    assert isinstance(example_provider(), NewExample)


def test_init_with_invalid_provided_type(singleton_cls):
    class ExampleProvider(singleton_cls):
        provided_type = Example

    with raises(errors.Error):
        ExampleProvider(list)


def test_provided_instance_provider(provider):
    assert isinstance(provider.provided, providers.ProvidedInstance)


def test_call(provider):
    instance1 = provider()
    instance2 = provider()

    assert instance1 is instance2
    assert isinstance(instance1, Example)
    assert isinstance(instance2, Example)


def test_call_with_init_positional_args(singleton_cls):
    provider = singleton_cls(Example, "i1", "i2")

    instance1 = provider()
    instance2 = provider()

    assert instance1.init_arg1 == "i1"
    assert instance1.init_arg2 == "i2"

    assert instance2.init_arg1 == "i1"
    assert instance2.init_arg2 == "i2"

    assert instance1 is instance2
    assert isinstance(instance1, Example)
    assert isinstance(instance2, Example)


def test_call_with_init_keyword_args(singleton_cls):
    provider = singleton_cls(Example, init_arg1="i1", init_arg2="i2")

    instance1 = provider()
    instance2 = provider()

    assert instance1.init_arg1 == "i1"
    assert instance1.init_arg2 == "i2"

    assert instance2.init_arg1 == "i1"
    assert instance2.init_arg2 == "i2"

    assert instance1 is instance2
    assert isinstance(instance1, Example)
    assert isinstance(instance2, Example)


def test_call_with_init_positional_and_keyword_args(singleton_cls):
    provider = singleton_cls(Example, "i1", init_arg2="i2")

    instance1 = provider()
    instance2 = provider()

    assert instance1.init_arg1 == "i1"
    assert instance1.init_arg2 == "i2"

    assert instance2.init_arg1 == "i1"
    assert instance2.init_arg2 == "i2"

    assert instance1 is instance2
    assert isinstance(instance1, Example)
    assert isinstance(instance2, Example)


def test_call_with_attributes(provider):
    provider.add_attributes(attribute1="a1", attribute2="a2")

    instance1 = provider()
    instance2 = provider()

    assert instance1.attribute1 == "a1"
    assert instance1.attribute2 == "a2"

    assert instance2.attribute1 == "a1"
    assert instance2.attribute2 == "a2"

    assert instance1 is instance2
    assert isinstance(instance1, Example)
    assert isinstance(instance2, Example)


def test_call_with_context_args(provider):
    instance = provider(11, 22)

    assert instance.init_arg1 == 11
    assert instance.init_arg2 == 22


def test_call_with_context_kwargs(singleton_cls):
    provider = singleton_cls(Example, init_arg1=1)

    instance1 = provider(init_arg2=22)
    assert instance1.init_arg1 == 1
    assert instance1.init_arg2 == 22

    # Instance is created earlier
    instance1 = provider(init_arg1=11, init_arg2=22)
    assert instance1.init_arg1 == 1
    assert instance1.init_arg2 == 22


def test_call_with_context_args_and_kwargs(singleton_cls):
    provider = singleton_cls(Example, 11)

    instance = provider(22, init_arg3=33, init_arg4=44)

    assert instance.init_arg1 == 11
    assert instance.init_arg2 == 22
    assert instance.init_arg3 == 33
    assert instance.init_arg4 == 44


def test_fluent_interface(singleton_cls):
    provider = singleton_cls(Example) \
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


def test_set_args(singleton_cls):
    provider = singleton_cls(Example) \
        .add_args(1, 2) \
        .set_args(3, 4)
    assert provider.args == (3, 4)


def test_set_kwargs(singleton_cls):
    provider = singleton_cls(Example) \
        .add_kwargs(init_arg3=3, init_arg4=4) \
        .set_kwargs(init_arg3=4, init_arg4=5)
    assert provider.kwargs == dict(init_arg3=4, init_arg4=5)


def test_set_attributes(singleton_cls):
    provider = singleton_cls(Example) \
        .add_attributes(attribute1=5, attribute2=6) \
        .set_attributes(attribute1=6, attribute2=7)
    assert provider.attributes == dict(attribute1=6, attribute2=7)


def test_clear_args(singleton_cls):
    provider = singleton_cls(Example) \
        .add_args(1, 2) \
        .clear_args()
    assert provider.args == tuple()


def test_clear_kwargs(singleton_cls):
    provider = singleton_cls(Example) \
        .add_kwargs(init_arg3=3, init_arg4=4) \
        .clear_kwargs()
    assert provider.kwargs == dict()


def test_clear_attributes(singleton_cls):
    provider = singleton_cls(Example) \
        .add_attributes(attribute1=5, attribute2=6) \
        .clear_attributes()
    assert provider.attributes == dict()


def test_call_overridden(singleton_cls):
    provider = singleton_cls(Example)
    overriding_provider1 = singleton_cls(dict)
    overriding_provider2 = singleton_cls(list)

    provider.override(overriding_provider1)
    provider.override(overriding_provider2)

    instance1 = provider()
    instance2 = provider()

    assert instance1 is instance2
    assert isinstance(instance1, list)
    assert isinstance(instance2, list)


def test_deepcopy(singleton_cls):
    provider = singleton_cls(Example)
    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert provider.cls is provider_copy.cls
    assert isinstance(provider, singleton_cls)


def test_deepcopy_from_memo(singleton_cls):
    provider = singleton_cls(Example)
    provider_copy_memo = singleton_cls(Example)

    provider_copy = providers.deepcopy(provider, memo={id(provider): provider_copy_memo})
    assert provider_copy is provider_copy_memo


def test_deepcopy_args(singleton_cls):
    provider = singleton_cls(Example)
    dependent_provider1 = singleton_cls(list)
    dependent_provider2 = singleton_cls(dict)

    provider.add_args(dependent_provider1, dependent_provider2)

    provider_copy = providers.deepcopy(provider)
    dependent_provider_copy1 = provider_copy.args[0]
    dependent_provider_copy2 = provider_copy.args[1]

    assert provider.args != provider_copy.args

    assert dependent_provider1.cls is dependent_provider_copy1.cls
    assert dependent_provider1 is not dependent_provider_copy1

    assert dependent_provider2.cls is dependent_provider_copy2.cls
    assert dependent_provider2 is not dependent_provider_copy2


def test_deepcopy_kwargs(singleton_cls):
    provider = singleton_cls(Example)
    dependent_provider1 = singleton_cls(list)
    dependent_provider2 = singleton_cls(dict)

    provider.add_kwargs(a1=dependent_provider1, a2=dependent_provider2)

    provider_copy = providers.deepcopy(provider)
    dependent_provider_copy1 = provider_copy.kwargs["a1"]
    dependent_provider_copy2 = provider_copy.kwargs["a2"]

    assert provider.kwargs != provider_copy.kwargs

    assert dependent_provider1.cls is dependent_provider_copy1.cls
    assert dependent_provider1 is not dependent_provider_copy1

    assert dependent_provider2.cls is dependent_provider_copy2.cls
    assert dependent_provider2 is not dependent_provider_copy2


def test_deepcopy_attributes(singleton_cls):
    provider = singleton_cls(Example)
    dependent_provider1 = singleton_cls(list)
    dependent_provider2 = singleton_cls(dict)

    provider.add_attributes(a1=dependent_provider1, a2=dependent_provider2)

    provider_copy = providers.deepcopy(provider)
    dependent_provider_copy1 = provider_copy.attributes["a1"]
    dependent_provider_copy2 = provider_copy.attributes["a2"]

    assert provider.attributes != provider_copy.attributes

    assert dependent_provider1.cls is dependent_provider_copy1.cls
    assert dependent_provider1 is not dependent_provider_copy1

    assert dependent_provider2.cls is dependent_provider_copy2.cls
    assert dependent_provider2 is not dependent_provider_copy2


def test_deepcopy_overridden(singleton_cls):
    provider = singleton_cls(Example)
    object_provider = providers.Object(object())

    provider.override(object_provider)

    provider_copy = providers.deepcopy(provider)
    object_provider_copy = provider_copy.overridden[0]

    assert provider is not provider_copy
    assert provider.cls is provider_copy.cls
    assert isinstance(provider, singleton_cls)

    assert object_provider is not object_provider_copy
    assert isinstance(object_provider_copy, providers.Object)


def test_deepcopy_with_sys_streams(singleton_cls):
    provider = singleton_cls(Example)
    provider.add_args(sys.stdin)
    provider.add_kwargs(a2=sys.stdout)
    provider.add_attributes(a3=sys.stderr)

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert isinstance(provider_copy, singleton_cls)
    assert provider.args[0] is sys.stdin
    assert provider.kwargs["a2"] is sys.stdout
    assert provider.attributes["a3"] is sys.stderr


def test_reset(singleton_cls):
    provider = singleton_cls(object)

    instance1 = provider()
    assert isinstance(instance1, object)

    provider.reset()

    instance2 = provider()
    assert isinstance(instance2, object)
    assert instance1 is not instance2


def test_reset_clean(provider):
    instance1 = provider()

    provider.reset()
    provider.reset()

    instance2 = provider()
    assert instance1 is not instance2


def test_reset_with_singleton(singleton_cls):
    dependent_singleton = providers.Singleton(object)
    provider = singleton_cls(dict, dependency=dependent_singleton)

    dependent_instance = dependent_singleton()
    instance1 = provider()
    assert instance1["dependency"] is dependent_instance

    provider.reset()

    instance2 = provider()
    assert instance2["dependency"] is dependent_instance
    assert instance1 is not instance2


def test_reset_context_manager(provider):
    instance1 = provider()
    with provider.reset():
        instance2 = provider()
    instance3 = provider()
    assert len({instance1, instance2, instance3}) == 3


def test_reset_context_manager_as_attribute(provider):
    with provider.reset() as alias:
        pass
    assert provider is alias


def test_full_reset(singleton_cls):
    dependent_singleton = providers.Singleton(object)
    provider = singleton_cls(dict, dependency=dependent_singleton)

    dependent_instance1 = dependent_singleton()
    instance1 = provider()
    assert instance1["dependency"] is dependent_instance1

    provider.full_reset()

    dependent_instance2 = dependent_singleton()
    instance2 = provider()
    assert instance2["dependency"] is not dependent_instance1
    assert dependent_instance1 is not dependent_instance2
    assert instance1 is not instance2


def test_full_reset_context_manager(singleton_cls):
    class Item:
        def __init__(self, dependency):
            self.dependency = dependency

    dependent_singleton = providers.Singleton(object)
    singleton = singleton_cls(Item, dependency=dependent_singleton)

    instance1 = singleton()
    with singleton.full_reset():
        instance2 = singleton()
    instance3 = singleton()

    assert len({instance1, instance2, instance3}) == 3
    assert len({instance1.dependency, instance2.dependency, instance3.dependency}) == 3


def test_full_reset_context_manager_as_attribute(provider):
    with provider.full_reset() as alias:
        pass
    assert provider is alias


def test_repr(provider):
    assert repr(provider) == (
        "<dependency_injector.providers."
        "{0}({1}) at {2}>".format(provider.__class__.__name__, repr(Example), hex(id(provider)))
    )
