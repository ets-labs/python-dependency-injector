"""Resource provider tests."""

import decimal
import sys
from typing import Any

from dependency_injector import containers, providers, resources, errors
from pytest import raises, mark


def init_fn(*args, **kwargs):
    return args, kwargs


def test_is_provider():
    assert providers.is_provider(providers.Resource(init_fn)) is True


def test_init_optional_provides():
    provider = providers.Resource()
    provider.set_provides(init_fn)
    assert provider.provides is init_fn
    assert provider() == (tuple(), dict())


def test_set_provides_returns_():
    provider = providers.Resource()
    assert provider.set_provides(init_fn) is provider


@mark.parametrize(
    "str_name,cls",
    [
        ("dependency_injector.providers.Factory", providers.Factory),
        ("decimal.Decimal", decimal.Decimal),
        ("list", list),
        (".test_resource_py35.test_is_provider", test_is_provider),
        ("test_is_provider", test_is_provider),
    ],
)
def test_set_provides_string_imports(str_name, cls):
    assert providers.Resource(str_name).provides is cls


def test_provided_instance_provider():
    provider = providers.Resource(init_fn)
    assert isinstance(provider.provided, providers.ProvidedInstance)


def test_injection():
    resource = object()

    def _init():
        _init.counter += 1
        return resource

    _init.counter = 0

    class Container(containers.DeclarativeContainer):
        resource = providers.Resource(_init)
        dependency1 = providers.List(resource)
        dependency2 = providers.List(resource)

    container = Container()
    list1 = container.dependency1()
    list2 = container.dependency2()

    assert list1 == [resource]
    assert list1[0] is resource

    assert list2 == [resource]
    assert list2[0] is resource

    assert _init.counter == 1


def test_init_function():
    def _init():
        _init.counter += 1

    _init.counter = 0

    provider = providers.Resource(_init)

    result1 = provider()
    assert result1 is None
    assert _init.counter == 1

    result2 = provider()
    assert result2 is None
    assert _init.counter == 1

    provider.shutdown()


def test_init_generator():
    def _init():
        _init.init_counter += 1
        yield
        _init.shutdown_counter += 1

    _init.init_counter = 0
    _init.shutdown_counter = 0

    provider = providers.Resource(_init)

    result1 = provider()
    assert result1 is None
    assert _init.init_counter == 1
    assert _init.shutdown_counter == 0

    provider.shutdown()
    assert _init.init_counter == 1
    assert _init.shutdown_counter == 1

    result2 = provider()
    assert result2 is None
    assert _init.init_counter == 2
    assert _init.shutdown_counter == 1

    provider.shutdown()
    assert _init.init_counter == 2
    assert _init.shutdown_counter == 2


def test_init_class():
    class TestResource(resources.Resource):
        init_counter = 0
        shutdown_counter = 0

        def init(self):
            self.__class__.init_counter += 1

        def shutdown(self, _):
            self.__class__.shutdown_counter += 1

    provider = providers.Resource(TestResource)

    result1 = provider()
    assert result1 is None
    assert TestResource.init_counter == 1
    assert TestResource.shutdown_counter == 0

    provider.shutdown()
    assert TestResource.init_counter == 1
    assert TestResource.shutdown_counter == 1

    result2 = provider()
    assert result2 is None
    assert TestResource.init_counter == 2
    assert TestResource.shutdown_counter == 1

    provider.shutdown()
    assert TestResource.init_counter == 2
    assert TestResource.shutdown_counter == 2


def test_init_class_generic_typing():
    # See issue: https://github.com/ets-labs/python-dependency-injector/issues/488
    class TestDependency:
        ...

    class TestResource(resources.Resource[TestDependency]):
        def init(self, *args: Any, **kwargs: Any) -> TestDependency:
            return TestDependency()

        def shutdown(self, resource: TestDependency) -> None: ...

    assert issubclass(TestResource, resources.Resource) is True


def test_init_class_abc_init_definition_is_required():
    class TestResource(resources.Resource):
        ...

    with raises(TypeError) as context:
        TestResource()

    assert "Can't instantiate abstract class TestResource" in str(context.value)
    assert "init" in str(context.value)


def test_init_class_abc_shutdown_definition_is_not_required():
    class TestResource(resources.Resource):
        def init(self):
            ...

    assert hasattr(TestResource(), "shutdown") is True


def test_init_not_callable():
    provider = providers.Resource(1)
    with raises(errors.Error):
        provider.init()


def test_init_and_shutdown():
    def _init():
        _init.init_counter += 1
        yield
        _init.shutdown_counter += 1

    _init.init_counter = 0
    _init.shutdown_counter = 0

    provider = providers.Resource(_init)

    result1 = provider.init()
    assert result1 is None
    assert _init.init_counter == 1
    assert _init.shutdown_counter == 0

    provider.shutdown()
    assert _init.init_counter == 1
    assert _init.shutdown_counter == 1

    result2 = provider.init()
    assert result2 is None
    assert _init.init_counter == 2
    assert _init.shutdown_counter == 1

    provider.shutdown()
    assert _init.init_counter == 2
    assert _init.shutdown_counter == 2


def test_shutdown_of_not_initialized():
    def _init():
        yield

    provider = providers.Resource(_init)

    result = provider.shutdown()
    assert result is None


def test_initialized():
    provider = providers.Resource(init_fn)
    assert provider.initialized is False

    provider.init()
    assert provider.initialized is True

    provider.shutdown()
    assert provider.initialized is False


def test_call_with_context_args():
    provider = providers.Resource(init_fn, "i1", "i2")
    assert provider("i3", i4=4) == (("i1", "i2", "i3"), {"i4": 4})


def test_fluent_interface():
    provider = providers.Resource(init_fn) \
        .add_args(1, 2) \
        .add_kwargs(a3=3, a4=4)
    assert provider() == ((1, 2), {"a3": 3, "a4": 4})


def test_set_args():
    provider = providers.Resource(init_fn) \
        .add_args(1, 2) \
        .set_args(3, 4)
    assert provider.args == (3, 4)


def test_clear_args():
    provider = providers.Resource(init_fn) \
        .add_args(1, 2) \
        .clear_args()
    assert provider.args == tuple()


def test_set_kwargs():
    provider = providers.Resource(init_fn) \
        .add_kwargs(a1="i1", a2="i2") \
        .set_kwargs(a3="i3", a4="i4")
    assert provider.kwargs == {"a3": "i3", "a4": "i4"}


def test_clear_kwargs():
    provider = providers.Resource(init_fn) \
        .add_kwargs(a1="i1", a2="i2") \
        .clear_kwargs()
    assert provider.kwargs == {}


def test_call_overridden():
    provider = providers.Resource(init_fn, 1)
    overriding_provider1 = providers.Resource(init_fn, 2)
    overriding_provider2 = providers.Resource(init_fn, 3)

    provider.override(overriding_provider1)
    provider.override(overriding_provider2)

    instance1 = provider()
    instance2 = provider()

    assert instance1 is instance2
    assert instance1 == ((3,), {})
    assert instance2 == ((3,), {})


def test_deepcopy():
    provider = providers.Resource(init_fn, 1, 2, a3=3, a4=4)

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert provider.args == provider_copy.args
    assert provider.kwargs == provider_copy.kwargs
    assert isinstance(provider, providers.Resource)


def test_deepcopy_initialized():
    provider = providers.Resource(init_fn)
    provider.init()

    with raises(errors.Error):
        providers.deepcopy(provider)


def test_deepcopy_from_memo():
    provider = providers.Resource(init_fn)
    provider_copy_memo = providers.Resource(init_fn)

    provider_copy = providers.deepcopy(
        provider,
        memo={id(provider): provider_copy_memo},
    )

    assert provider_copy is provider_copy_memo


def test_deepcopy_args():
    provider = providers.Resource(init_fn)
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
    provider = providers.Resource(init_fn)
    dependent_provider1 = providers.Factory(list)
    dependent_provider2 = providers.Factory(dict)

    provider.add_kwargs(d1=dependent_provider1, d2=dependent_provider2)

    provider_copy = providers.deepcopy(provider)
    dependent_provider_copy1 = provider_copy.kwargs["d1"]
    dependent_provider_copy2 = provider_copy.kwargs["d2"]

    assert provider.kwargs != provider_copy.kwargs

    assert dependent_provider1.cls is dependent_provider_copy1.cls
    assert dependent_provider1 is not dependent_provider_copy1

    assert dependent_provider2.cls is dependent_provider_copy2.cls
    assert dependent_provider2 is not dependent_provider_copy2


def test_deepcopy_overridden():
    provider = providers.Resource(init_fn)
    object_provider = providers.Object(object())

    provider.override(object_provider)

    provider_copy = providers.deepcopy(provider)
    object_provider_copy = provider_copy.overridden[0]

    assert provider is not provider_copy
    assert provider.args == provider_copy.args
    assert isinstance(provider, providers.Resource)

    assert object_provider is not object_provider_copy
    assert isinstance(object_provider_copy, providers.Object)


def test_deepcopy_with_sys_streams():
    provider = providers.Resource(init_fn)
    provider.add_args(sys.stdin, sys.stdout, sys.stderr)

    provider_copy = providers.deepcopy(provider)

    assert provider is not provider_copy
    assert isinstance(provider_copy, providers.Resource)
    assert provider.args[0] is sys.stdin
    assert provider.args[1] is sys.stdout
    assert provider.args[2] is sys.stderr


def test_repr():
    provider = providers.Resource(init_fn)

    assert repr(provider) == (
        "<dependency_injector.providers.Resource({0}) at {1}>".format(
            repr(init_fn),
            hex(id(provider)),
        )
    )
