"""Configuration.from_env() tests."""

from pytest import mark, raises


def test(config):
    config.from_env("CONFIG_TEST_ENV")
    assert config() == "test-value"


def test_with_children(config):
    config.section1.value1.from_env("CONFIG_TEST_ENV")

    assert config() == {"section1": {"value1": "test-value"}}
    assert config.section1() == {"value1": "test-value"}
    assert config.section1.value1() == "test-value"


def test_default(config):
    config.from_env("UNDEFINED_ENV", "default-value")
    assert config() == "default-value"


def test_default_none(config):
    config.from_env("UNDEFINED_ENV")
    assert config() is None


def test_option_default_none(config):
    config.option.from_env("UNDEFINED_ENV")
    assert config.option() is None


def test_as_(config):
    config.from_env("CONFIG_INT", as_=int)
    assert config() == 42
    assert isinstance(config(), int)


def test_as__default(config):
    config.from_env("UNDEFINED", as_=int, default="33")
    assert config() == 33
    assert isinstance(config(), int)


def test_as__undefined_required(config):
    with raises(ValueError):
        config.from_env("UNDEFINED", as_=int, required=True)
    assert config() == {}


def test_as__defined_empty(config):
    with raises(ValueError):
        config.from_env("EMPTY", as_=int)
    assert config() == {}


def test_option_as_(config):
    config.option.from_env("CONFIG_INT", as_=int)
    assert config.option() == 42
    assert isinstance(config.option(), int)


def test_option_as__default(config):
    config.option.from_env("UNDEFINED", as_=int, default="33")
    assert config.option() == 33
    assert isinstance(config.option(), int)


def test_option_as__undefined_required(config):
    with raises(ValueError):
        config.option.from_env("UNDEFINED", as_=int, required=True)
    assert config.option() is None


def test_option_as__defined_empty(config):
    with raises(ValueError):
        config.option.from_env("EMPTY", as_=int)
    assert config.option() is None


@mark.parametrize("config_type", ["strict"])
def test_undefined_in_strict_mode(config):
    with raises(ValueError):
        config.from_env("UNDEFINED_ENV")


@mark.parametrize("config_type", ["strict"])
def test_option_undefined_in_strict_mode(config):
    with raises(ValueError):
        config.option.from_env("UNDEFINED_ENV")


def test_undefined_in_strict_mode_with_default(config):
    config.from_env("UNDEFINED_ENV", "default-value")
    assert config() == "default-value"


@mark.parametrize("config_type", ["strict"])
def test_option_undefined_in_strict_mode_with_default(config):
    config.option.from_env("UNDEFINED_ENV", "default-value")
    assert config.option() == "default-value"


def test_required_undefined(config):
    with raises(ValueError):
        config.from_env("UNDEFINED_ENV", required=True)


def test_required_undefined_with_default(config):
    config.from_env("UNDEFINED_ENV", default="default-value", required=True)
    assert config() == "default-value"


def test_option_required_undefined(config):
    with raises(ValueError):
        config.option.from_env("UNDEFINED_ENV", required=True)


def test_option_required_undefined_with_default(config):
    config.option.from_env("UNDEFINED_ENV", default="default-value", required=True)
    assert config.option() == "default-value"


@mark.parametrize("config_type", ["strict"])
def test_not_required_undefined_in_strict_mode(config):
    config.from_env("UNDEFINED_ENV", required=False)
    assert config() is None


@mark.parametrize("config_type", ["strict"])
def test_option_not_required_undefined_in_strict_mode(config):
    config.option.from_env("UNDEFINED_ENV", required=False)
    assert config.option() is None


@mark.parametrize("config_type", ["strict"])
def test_not_required_undefined_with_default_in_strict_mode(config):
    config.from_env("UNDEFINED_ENV", default="default-value", required=False)
    assert config() == "default-value"


@mark.parametrize("config_type", ["strict"])
def test_option_not_required_undefined_with_default_in_strict_mode(config):
    config.option.from_env("UNDEFINED_ENV", default="default-value", required=False)
    assert config.option() == "default-value"
