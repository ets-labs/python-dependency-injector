"""Aggregate provider tests."""

from dependency_injector import providers, errors
from pytest import fixture, mark, raises


class Example:
    def __init__(self, init_arg1=None, init_arg2=None, init_arg3=None, init_arg4=None):
        self.init_arg1 = init_arg1
        self.init_arg2 = init_arg2
        self.init_arg3 = init_arg3
        self.init_arg4 = init_arg4

        self.attribute1 = None
        self.attribute2 = None


class ExampleA(Example):
    pass


class ExampleB(Example):
    pass


@fixture
def factory_a():
    return providers.Factory(ExampleA)


@fixture
def factory_b():
    return providers.Factory(ExampleB)


@fixture
def aggregate_type():
    return "default"


@fixture
def aggregate(aggregate_type, factory_a, factory_b):
    if aggregate_type == "empty":
        return providers.Aggregate()
    elif aggregate_type == "non-string-keys":
        return providers.Aggregate({
            ExampleA: factory_a,
            ExampleB: factory_b,
        })
    elif aggregate_type == "default":
        return providers.Aggregate(
            example_a=factory_a,
            example_b=factory_b,
        )
    else:
        raise ValueError("Unknown factory type \"{0}\"".format(aggregate_type))


def test_is_provider(aggregate):
    assert providers.is_provider(aggregate) is True


def test_is_delegated_provider(aggregate):
    assert providers.is_delegated(aggregate) is True


@mark.parametrize("aggregate_type", ["non-string-keys"])
def test_init_with_non_string_keys(aggregate, factory_a, factory_b):
    object_a = aggregate(ExampleA, 1, 2, init_arg3=3, init_arg4=4)
    object_b = aggregate(ExampleB, 11, 22, init_arg3=33, init_arg4=44)

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

    assert aggregate.providers == {
        ExampleA: factory_a,
        ExampleB: factory_b,
    }


def test_init_with_not_a_factory():
    with raises(errors.Error):
        providers.Aggregate(
            example_a=providers.Factory(ExampleA),
            example_b=object(),
        )


@mark.parametrize("aggregate_type", ["empty"])
def test_init_optional_providers(aggregate, factory_a, factory_b):
    aggregate.set_providers(
        example_a=factory_a,
        example_b=factory_b,
    )
    assert aggregate.providers == {
        "example_a": factory_a,
        "example_b": factory_b,
    }
    assert isinstance(aggregate("example_a"), ExampleA)
    assert isinstance(aggregate("example_b"), ExampleB)


@mark.parametrize("aggregate_type", ["non-string-keys"])
def test_set_providers_with_non_string_keys(aggregate, factory_a, factory_b):
    aggregate.set_providers({
        ExampleA: factory_a,
        ExampleB: factory_b,
    })

    object_a = aggregate(ExampleA, 1, 2, init_arg3=3, init_arg4=4)
    object_b = aggregate(ExampleB, 11, 22, init_arg3=33, init_arg4=44)

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

    assert aggregate.providers == {
        ExampleA: factory_a,
        ExampleB: factory_b,
    }


def test_set_providers_returns_self(aggregate, factory_a):
    assert aggregate.set_providers(example_a=factory_a) is aggregate


@mark.parametrize("aggregate_type", ["empty"])
def test_init_optional_providers(aggregate, factory_a, factory_b):
    aggregate.set_providers(
        example_a=factory_a,
        example_b=factory_b,
    )
    assert aggregate.providers == {
        "example_a": factory_a,
        "example_b": factory_b,
    }
    assert isinstance(aggregate("example_a"), ExampleA)
    assert isinstance(aggregate("example_b"), ExampleB)


@mark.parametrize("aggregate_type", ["non-string-keys"])
def test_set_providers_with_non_string_keys(aggregate, factory_a, factory_b):
    aggregate.set_providers({
        ExampleA: factory_a,
        ExampleB: factory_b,
    })

    object_a = aggregate(ExampleA, 1, 2, init_arg3=3, init_arg4=4)
    object_b = aggregate(ExampleB, 11, 22, init_arg3=33, init_arg4=44)

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

    assert aggregate.providers == {
        ExampleA: factory_a,
        ExampleB: factory_b,
    }


def test_set_providers_returns_self(aggregate, factory_a):
    assert aggregate.set_providers(example_a=factory_a) is aggregate


def test_call(aggregate):
    object_a = aggregate("example_a", 1, 2, init_arg3=3, init_arg4=4)
    object_b = aggregate("example_b", 11, 22, init_arg3=33, init_arg4=44)

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


def test_call_factory_name_as_kwarg(aggregate):
    object_a = aggregate(
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


def test_call_no_factory_name(aggregate):
    with raises(TypeError):
        aggregate()


def test_call_no_such_provider(aggregate):
    with raises(errors.NoSuchProviderError):
        aggregate("unknown")


def test_overridden(aggregate):
    with raises(errors.Error):
        aggregate.override(providers.Object(object()))


def test_getattr(aggregate, factory_a, factory_b):
    assert aggregate.example_a is factory_a
    assert aggregate.example_b is factory_b


def test_getattr_no_such_provider(aggregate):
    with raises(errors.NoSuchProviderError):
        aggregate.unknown


def test_providers(aggregate, factory_a, factory_b):
    assert aggregate.providers == dict(
        example_a=factory_a,
        example_b=factory_b,
    )


def test_deepcopy(aggregate):
    provider_copy = providers.deepcopy(aggregate)

    assert aggregate is not provider_copy
    assert isinstance(provider_copy, type(aggregate))

    assert aggregate.example_a is not provider_copy.example_a
    assert isinstance(aggregate.example_a, type(provider_copy.example_a))
    assert aggregate.example_a.cls is provider_copy.example_a.cls

    assert aggregate.example_b is not provider_copy.example_b
    assert isinstance(aggregate.example_b, type(provider_copy.example_b))
    assert aggregate.example_b.cls is provider_copy.example_b.cls


@mark.parametrize("aggregate_type", ["non-string-keys"])
def test_deepcopy_with_non_string_keys(aggregate):
    provider_copy = providers.deepcopy(aggregate)

    assert aggregate is not provider_copy
    assert isinstance(provider_copy, type(aggregate))

    assert aggregate.providers[ExampleA] is not provider_copy.providers[ExampleA]
    assert isinstance(aggregate.providers[ExampleA], type(provider_copy.providers[ExampleA]))
    assert aggregate.providers[ExampleA].provides is provider_copy.providers[ExampleA].provides

    assert aggregate.providers[ExampleB] is not provider_copy.providers[ExampleB]
    assert isinstance(aggregate.providers[ExampleB], type(provider_copy.providers[ExampleB]))
    assert aggregate.providers[ExampleB].provides is provider_copy.providers[ExampleB].provides


def test_repr(aggregate):
    assert repr(aggregate) == (
        "<dependency_injector.providers."
        "Aggregate({0}) at {1}>".format(
            repr(aggregate.providers),
            hex(id(aggregate)),
        )
    )
