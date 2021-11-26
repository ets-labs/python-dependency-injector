"""FactoryAggregate provider tests."""

from dependency_injector import providers, errors
from pytest import fixture, mark, raises

from .common import ExampleA, ExampleB


@fixture
def factory_a():
    return providers.Factory(ExampleA)


@fixture
def factory_b():
    return providers.Factory(ExampleB)


@fixture
def factory_type():
    return "default"


@fixture
def factory_aggregate(factory_type, factory_a, factory_b):
    if factory_type == "empty":
        return providers.FactoryAggregate()
    elif factory_type == "non-string-keys":
        return providers.FactoryAggregate({
            ExampleA: factory_a,
            ExampleB: factory_b,
        })
    elif factory_type == "default":
        return providers.FactoryAggregate(
            example_a=factory_a,
            example_b=factory_b,
        )
    else:
        raise ValueError("Unknown factory type \"{0}\"".format(factory_type))


def test_is_provider(factory_aggregate):
    assert providers.is_provider(factory_aggregate) is True


def test_is_delegated_provider(factory_aggregate):
    assert providers.is_delegated(factory_aggregate) is True


@mark.parametrize("factory_type", ["non-string-keys"])
def test_init_with_non_string_keys(factory_aggregate, factory_a, factory_b):
    object_a = factory_aggregate(ExampleA, 1, 2, init_arg3=3, init_arg4=4)
    object_b = factory_aggregate(ExampleB, 11, 22, init_arg3=33, init_arg4=44)

    assert isinstance(object_a, ExampleA)
    assert object_a.init_arg1 == 1
    assert object_a.init_arg2 == 2
    assert object_a.init_arg3 == 3
    assert object_a.init_arg4 == 4

    assert isinstance(object_b, ExampleB)
    assert object_b.init_arg1 == 11
    assert object_b.init_arg2 == 22
    assert object_b.init_arg3 == 33
    assert object_b.init_arg4 == 44

    assert factory_aggregate.factories == {
        ExampleA: factory_a,
        ExampleB: factory_b,
    }


def test_init_with_not_a_factory():
    with raises(errors.Error):
        providers.FactoryAggregate(
            example_a=providers.Factory(ExampleA),
            example_b=object(),
        )


@mark.parametrize("factory_type", ["empty"])
def test_init_optional_providers(factory_aggregate, factory_a, factory_b):
    factory_aggregate.set_providers(
        example_a=factory_a,
        example_b=factory_b,
    )
    assert factory_aggregate.providers == {
        "example_a": factory_a,
        "example_b": factory_b,
    }
    assert isinstance(factory_aggregate("example_a"), ExampleA)
    assert isinstance(factory_aggregate("example_b"), ExampleB)


@mark.parametrize("factory_type", ["non-string-keys"])
def test_set_factories_with_non_string_keys(factory_aggregate, factory_a, factory_b):
    factory_aggregate.set_providers({
        ExampleA: factory_a,
        ExampleB: factory_b,
    })

    object_a = factory_aggregate(ExampleA, 1, 2, init_arg3=3, init_arg4=4)
    object_b = factory_aggregate(ExampleB, 11, 22, init_arg3=33, init_arg4=44)

    assert isinstance(object_a, ExampleA)
    assert object_a.init_arg1 == 1
    assert object_a.init_arg2 == 2
    assert object_a.init_arg3 == 3
    assert object_a.init_arg4 == 4

    assert isinstance(object_b, ExampleB)
    assert object_b.init_arg1 == 11
    assert object_b.init_arg2 == 22
    assert object_b.init_arg3 == 33
    assert object_b.init_arg4 == 44

    assert factory_aggregate.providers == {
        ExampleA: factory_a,
        ExampleB: factory_b,
    }


def test_set_providers_returns_self(factory_aggregate, factory_a):
    assert factory_aggregate.set_providers(example_a=factory_a) is factory_aggregate


@mark.parametrize("factory_type", ["empty"])
def test_init_optional_factories(factory_aggregate, factory_a, factory_b):
    factory_aggregate.set_factories(
        example_a=factory_a,
        example_b=factory_b,
    )
    assert factory_aggregate.factories == {
        "example_a": factory_a,
        "example_b": factory_b,
    }
    assert isinstance(factory_aggregate("example_a"), ExampleA)
    assert isinstance(factory_aggregate("example_b"), ExampleB)


@mark.parametrize("factory_type", ["non-string-keys"])
def test_set_factories_with_non_string_keys(factory_aggregate, factory_a, factory_b):
    factory_aggregate.set_factories({
        ExampleA: factory_a,
        ExampleB: factory_b,
    })

    object_a = factory_aggregate(ExampleA, 1, 2, init_arg3=3, init_arg4=4)
    object_b = factory_aggregate(ExampleB, 11, 22, init_arg3=33, init_arg4=44)

    assert isinstance(object_a, ExampleA)
    assert object_a.init_arg1 == 1
    assert object_a.init_arg2 == 2
    assert object_a.init_arg3 == 3
    assert object_a.init_arg4 == 4

    assert isinstance(object_b, ExampleB)
    assert object_b.init_arg1 == 11
    assert object_b.init_arg2 == 22
    assert object_b.init_arg3 == 33
    assert object_b.init_arg4 == 44

    assert factory_aggregate.factories == {
        ExampleA: factory_a,
        ExampleB: factory_b,
    }


def test_set_factories_returns_self(factory_aggregate, factory_a):
    assert factory_aggregate.set_factories(example_a=factory_a) is factory_aggregate


def test_call(factory_aggregate):
    object_a = factory_aggregate("example_a", 1, 2, init_arg3=3, init_arg4=4)
    object_b = factory_aggregate("example_b", 11, 22, init_arg3=33, init_arg4=44)

    assert isinstance(object_a, ExampleA)
    assert object_a.init_arg1 == 1
    assert object_a.init_arg2 == 2
    assert object_a.init_arg3 == 3
    assert object_a.init_arg4 == 4

    assert isinstance(object_b, ExampleB)
    assert object_b.init_arg1 == 11
    assert object_b.init_arg2 == 22
    assert object_b.init_arg3 == 33
    assert object_b.init_arg4 == 44


def test_call_factory_name_as_kwarg(factory_aggregate):
    object_a = factory_aggregate(
        factory_name="example_a",
        init_arg1=1,
        init_arg2=2,
        init_arg3=3,
        init_arg4=4,
    )
    assert isinstance(object_a, ExampleA)
    assert object_a.init_arg1 == 1
    assert object_a.init_arg2 == 2
    assert object_a.init_arg3 == 3
    assert object_a.init_arg4 == 4


def test_call_no_factory_name(factory_aggregate):
    with raises(TypeError):
        factory_aggregate()


def test_call_no_such_provider(factory_aggregate):
    with raises(errors.NoSuchProviderError):
        factory_aggregate("unknown")


def test_overridden(factory_aggregate):
    with raises(errors.Error):
        factory_aggregate.override(providers.Object(object()))


def test_getattr(factory_aggregate, factory_a, factory_b):
    assert factory_aggregate.example_a is factory_a
    assert factory_aggregate.example_b is factory_b


def test_getattr_no_such_provider(factory_aggregate):
    with raises(errors.NoSuchProviderError):
        factory_aggregate.unknown


def test_factories(factory_aggregate, factory_a, factory_b):
    assert factory_aggregate.factories == dict(
        example_a=factory_a,
        example_b=factory_b,
    )


def test_deepcopy(factory_aggregate):
    provider_copy = providers.deepcopy(factory_aggregate)

    assert factory_aggregate is not provider_copy
    assert isinstance(provider_copy, type(factory_aggregate))

    assert factory_aggregate.example_a is not provider_copy.example_a
    assert isinstance(factory_aggregate.example_a, type(provider_copy.example_a))
    assert factory_aggregate.example_a.cls is provider_copy.example_a.cls

    assert factory_aggregate.example_b is not provider_copy.example_b
    assert isinstance(factory_aggregate.example_b, type(provider_copy.example_b))
    assert factory_aggregate.example_b.cls is provider_copy.example_b.cls


@mark.parametrize("factory_type", ["non-string-keys"])
def test_deepcopy_with_non_string_keys(factory_aggregate):
    provider_copy = providers.deepcopy(factory_aggregate)

    assert factory_aggregate is not provider_copy
    assert isinstance(provider_copy, type(factory_aggregate))

    assert factory_aggregate.factories[ExampleA] is not provider_copy.factories[ExampleA]
    assert isinstance(factory_aggregate.factories[ExampleA], type(provider_copy.factories[ExampleA]))
    assert factory_aggregate.factories[ExampleA].cls is provider_copy.factories[ExampleA].cls

    assert factory_aggregate.factories[ExampleB] is not provider_copy.factories[ExampleB]
    assert isinstance(factory_aggregate.factories[ExampleB], type(provider_copy.factories[ExampleB]))
    assert factory_aggregate.factories[ExampleB].cls is provider_copy.factories[ExampleB].cls


def test_repr(factory_aggregate):
    assert repr(factory_aggregate) == (
        "<dependency_injector.providers."
        "FactoryAggregate({0}) at {1}>".format(
            repr(factory_aggregate.factories),
            hex(id(factory_aggregate)),
        )
    )
