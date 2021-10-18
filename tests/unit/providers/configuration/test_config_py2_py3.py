"""Configuration provider tests."""

import decimal

from dependency_injector import containers, providers, errors
from pytest import mark, raises


def test_init_optional(config):
    config.set_name("myconfig")
    config.set_default({"foo": "bar"})
    config.set_strict(True)

    assert config.get_name() == "myconfig"
    assert config.get_default() == {"foo": "bar"}
    assert config.get_strict() is True


def test_set_name_returns_self(config):
    assert config.set_name("myconfig") is config


def test_set_default_returns_self(config):
    assert config.set_default({}) is config


def test_set_strict_returns_self(config):
    assert config.set_strict(True) is config


def test_default_name(config):
    assert config.get_name() == "config"


def test_providers_are_providers(config):
    assert providers.is_provider(config.a) is True
    assert providers.is_provider(config.a.b) is True
    assert providers.is_provider(config.a.b.c) is True
    assert providers.is_provider(config.a.b.d) is True


def test_providers_are_not_delegates(config):
    assert providers.is_delegated(config.a) is False
    assert providers.is_delegated(config.a.b) is False
    assert providers.is_delegated(config.a.b.c) is False
    assert providers.is_delegated(config.a.b.d) is False


def test_providers_identity(config):
    assert config.a is config.a
    assert config.a.b is config.a.b
    assert config.a.b.c is config.a.b.c
    assert config.a.b.d is config.a.b.d


def test_get_name(config):
    assert config.a.b.c.get_name() == "config.a.b.c"


def test_providers_value_setting(config):
    a = config.a
    ab = config.a.b
    abc = config.a.b.c
    abd = config.a.b.d

    config.update({"a": {"b": {"c": 1, "d": 2}}})

    assert a() == {"b": {"c": 1, "d": 2}}
    assert ab() == {"c": 1, "d": 2}
    assert abc() == 1
    assert abd() == 2


def test_providers_with_already_set_value(config):
    config.update({"a": {"b": {"c": 1, "d": 2}}})

    a = config.a
    ab = config.a.b
    abc = config.a.b.c
    abd = config.a.b.d

    assert a() == {"b": {"c": 1, "d": 2}}
    assert ab() == {"c": 1, "d": 2}
    assert abc() == 1
    assert abd() == 2


def test_as_int(config):
    value_provider = providers.Callable(lambda value: value, config.test.as_int())
    config.from_dict({"test": "123"})

    value = value_provider()
    assert value == 123


def test_as_float(config):
    value_provider = providers.Callable(lambda value: value, config.test.as_float())
    config.from_dict({"test": "123.123"})

    value = value_provider()
    assert value == 123.123


def test_as_(config):
    value_provider = providers.Callable(
        lambda value: value,
        config.test.as_(decimal.Decimal),
    )
    config.from_dict({"test": "123.123"})

    value = value_provider()
    assert value == decimal.Decimal("123.123")


def test_required(config):
    provider = providers.Callable(
        lambda value: value,
        config.a.required(),
    )
    with raises(errors.Error, match="Undefined configuration option \"config.a\""):
        provider()


def test_required_defined_none(config):
    provider = providers.Callable(
        lambda value: value,
        config.a.required(),
    )
    config.from_dict({"a": None})
    assert provider() is None


def test_required_no_side_effect(config):
    _ = providers.Callable(
        lambda value: value,
        config.a.required(),
    )
    assert config.a() is None


def test_required_as_(config):
    provider = providers.List(
        config.int_test.required().as_int(),
        config.float_test.required().as_float(),
        config._as_test.required().as_(decimal.Decimal),
    )
    config.from_dict({"int_test": "1", "float_test": "2.0", "_as_test": "3.0"})
    assert provider() == [1, 2.0, decimal.Decimal("3.0")]


def test_providers_value_override(config):
    a = config.a
    ab = config.a.b
    abc = config.a.b.c
    abd = config.a.b.d

    config.override({"a": {"b": {"c": 1, "d": 2}}})

    assert a() == {"b": {"c": 1, "d": 2}}
    assert ab() == {"c": 1, "d": 2}
    assert abc() == 1
    assert abd() == 2


def test_configuration_option_override_and_reset_override(config):
    # Bug: https://github.com/ets-labs/python-dependency-injector/issues/319
    config.from_dict({"a": {"b": {"c": 1}}})

    assert config.a.b.c() == 1

    with config.set("a.b.c", "xxx"):
        assert config.a.b.c() == "xxx"
    assert config.a.b.c() == 1

    with config.a.b.c.override("yyy"):
        assert config.a.b.c() == "yyy"

    assert config.a.b.c() == 1


def test_providers_with_already_overridden_value(config):
    config.override({"a": {"b": {"c": 1, "d": 2}}})

    a = config.a
    ab = config.a.b
    abc = config.a.b.c
    abd = config.a.b.d

    assert a() == {"b": {"c": 1, "d": 2}}
    assert ab() == {"c": 1, "d": 2}
    assert abc() == 1
    assert abd() == 2


def test_providers_with_default_value(config):
    config.set_default({"a": {"b": {"c": 1, "d": 2}}})

    a = config.a
    ab = config.a.b
    abc = config.a.b.c
    abd = config.a.b.d

    assert a() == {"b": {"c": 1, "d": 2}}
    assert ab() == {"c": 1, "d": 2}
    assert abc() == 1
    assert abd() == 2


def test_providers_with_default_value_overriding(config):
    config.set_default({"a": {"b": {"c": 1, "d": 2}}})

    assert config.a() == {"b": {"c": 1, "d": 2}}
    assert config.a.b() == {"c": 1, "d": 2}
    assert config.a.b.c() == 1
    assert config.a.b.d() == 2

    config.override({"a": {"b": {"c": 3, "d": 4}}})
    assert config.a() == {"b": {"c": 3, "d": 4}}
    assert config.a.b() == {"c": 3, "d": 4}
    assert config.a.b.c() == 3
    assert config.a.b.d() == 4

    config.reset_override()
    assert config.a() == {"b": {"c": 1, "d": 2}}
    assert config.a.b() == {"c": 1, "d": 2}
    assert config.a.b.c() == 1
    assert config.a.b.d() == 2


def test_value_of_undefined_option(config):
    assert config.option() is None


@mark.parametrize("config_type", ["strict"])
def test_value_of_undefined_option_in_strict_mode(config):
    with raises(errors.Error, match="Undefined configuration option \"config.option\""):
        config.option()


@mark.parametrize("config_type", ["strict"])
def test_value_of_undefined_option_with_root_none_in_strict_mode(config):
    config.override(None)
    with raises(errors.Error, match="Undefined configuration option \"config.option\""):
        config.option()


@mark.parametrize("config_type", ["strict"])
def test_value_of_defined_none_option_in_strict_mode(config):
    config.from_dict({"a": None})
    assert config.a() is None


def test_getting_of_special_attributes(config):
    with raises(AttributeError):
        config.__name__


def test_getting_of_special_attributes_from_child(config):
    with raises(AttributeError):
        config.child.__name__


def test_context_manager_alias():
    class Container(containers.DeclarativeContainer):
        config = providers.Configuration()

    container = Container()

    with container.config as config:
        config.override({"foo": "foo", "bar": "bar"})

    assert container.config() == {"foo": "foo", "bar": "bar"}
    assert config() == {"foo": "foo", "bar": "bar"}
    assert container.config is config


def test_option_context_manager_alias():
    class Container(containers.DeclarativeContainer):
        config = providers.Configuration()

    container = Container()

    with container.config.option as option:
        option.override({"foo": "foo", "bar": "bar"})

    assert container.config() == {"option": {"foo": "foo", "bar": "bar"}}
    assert container.config.option() == {"foo": "foo", "bar": "bar"}
    assert option() == {"foo": "foo", "bar": "bar"}
    assert container.config.option is option


def test_missing_key(config):
    # See: https://github.com/ets-labs/python-dependency-injector/issues/358
    config.override(None)
    value = config.key()
    assert value is None


def test_deepcopy(config):
    config_copy = providers.deepcopy(config)
    assert isinstance(config_copy, providers.Configuration)
    assert config is not config_copy


def test_deepcopy_from_memo(config):
    config_copy_memo = providers.Configuration()

    provider_copy = providers.deepcopy(config, memo={id(config): config_copy_memo})
    assert provider_copy is config_copy_memo


def test_deepcopy_overridden(config):
    object_provider = providers.Object(object())

    config.override(object_provider)

    provider_copy = providers.deepcopy(config)
    object_provider_copy = provider_copy.overridden[0]

    assert config is not provider_copy
    assert isinstance(config, providers.Configuration)

    assert object_provider is not object_provider_copy
    assert isinstance(object_provider_copy, providers.Object)


def test_repr(config):
    assert repr(config) == (
        "<dependency_injector.providers."
        "Configuration({0}) at {1}>".format(repr("config"), hex(id(config)))
    )


def test_repr_child(config):
    assert repr(config.a.b.c) == (
        "<dependency_injector.providers."
        "ConfigurationOption({0}) at {1}>".format(repr("config.a.b.c"), hex(id(config.a.b.c)))
    )
