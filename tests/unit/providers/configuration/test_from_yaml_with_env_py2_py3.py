"""Configuration.from_yaml() with environment variables interpolation tests."""

import os

import yaml
from pytest import fixture, mark, raises


@fixture
def config_file(tmp_path):
    config_file = str(tmp_path / "config_1.ini")
    with open(config_file, "w") as file:
        file.write(
            "section1:\n"
            "  value1: ${CONFIG_TEST_ENV}\n"
            "  value2: ${CONFIG_TEST_PATH}/path\n"
        )
    return config_file


@fixture(autouse=True)
def environment_variables():
    os.environ["CONFIG_TEST_ENV"] = "test-value"
    os.environ["CONFIG_TEST_PATH"] = "test-path"
    os.environ["DEFINED"] = "defined"
    yield
    os.environ.pop("CONFIG_TEST_ENV", None)
    os.environ.pop("CONFIG_TEST_PATH", None)
    os.environ.pop("DEFINED", None)


def test_env_variable_interpolation(config, config_file):
    config.from_yaml(config_file)

    assert config() == {
        "section1": {
            "value1": "test-value",
            "value2": "test-path/path",
        },
    }
    assert config.section1() == {
        "value1": "test-value",
        "value2": "test-path/path",
    }
    assert config.section1.value1() == "test-value"
    assert config.section1.value2() == "test-path/path"


def test_missing_envs_not_required(config, config_file):
    del os.environ["CONFIG_TEST_ENV"]
    del os.environ["CONFIG_TEST_PATH"]

    config.from_yaml(config_file)

    assert config() == {
        "section1": {
            "value1": None,
            "value2": "/path",
        },
    }
    assert config.section1() == {
        "value1": None,
        "value2": "/path",
    }
    assert config.section1.value1() is None
    assert config.section1.value2() == "/path"


def test_missing_envs_required(config, config_file):
    with open(config_file, "w") as file:
        file.write(
            "section:\n"
            "  undefined: ${UNDEFINED}\n"
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.from_yaml(config_file, envs_required=True)


@mark.parametrize("config_type", ["strict"])
def test_missing_envs_strict_mode(config, config_file):
    with open(config_file, "w") as file:
        file.write(
            "section:\n"
            "  undefined: ${UNDEFINED}\n"
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.from_yaml(config_file)


def test_option_missing_envs_not_required(config, config_file):
    del os.environ["CONFIG_TEST_ENV"]
    del os.environ["CONFIG_TEST_PATH"]

    config.option.from_yaml(config_file)

    assert config.option() == {
        "section1": {
            "value1": None,
            "value2": "/path",
        },
    }
    assert config.option.section1() == {
        "value1": None,
        "value2": "/path",
    }
    assert config.option.section1.value1() is None
    assert config.option.section1.value2() == "/path"


def test_option_missing_envs_required(config, config_file):
    with open(config_file, "w") as file:
        file.write(
            "section:\n"
            "  undefined: ${UNDEFINED}\n"
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.option.from_yaml(config_file, envs_required=True)


@mark.parametrize("config_type", ["strict"])
def test_option_missing_envs_strict_mode(config, config_file):
    with open(config_file, "w") as file:
        file.write(
            "section:\n"
            "  undefined: ${UNDEFINED}\n"
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.option.from_yaml(config_file)


def test_default_values(config, config_file):
    with open(config_file, "w") as file:
        file.write(
            "section:\n"
            "  defined_with_default: ${DEFINED:default}\n"
            "  undefined_with_default: ${UNDEFINED:default}\n"
            "  complex: ${DEFINED}/path/${DEFINED:default}/${UNDEFINED}/${UNDEFINED:default}\n"
        )

    config.from_yaml(config_file)

    assert config.section() == {
        "defined_with_default": "defined",
        "undefined_with_default": "default",
        "complex": "defined/path/defined//default",
    }


def test_option_env_variable_interpolation(config, config_file):
    config.option.from_yaml(config_file)

    assert config.option() == {
        "section1": {
            "value1": "test-value",
            "value2": "test-path/path",
        },
    }
    assert config.option.section1() == {
        "value1": "test-value",
        "value2": "test-path/path",
    }
    assert config.option.section1.value1() == "test-value"
    assert config.option.section1.value2() == "test-path/path"


def test_env_variable_interpolation_custom_loader(config, config_file):
    config.from_yaml(config_file, loader=yaml.UnsafeLoader)

    assert config.section1() == {
        "value1": "test-value",
        "value2": "test-path/path",
    }
    assert config.section1.value1() == "test-value"
    assert config.section1.value2() == "test-path/path"


def test_option_env_variable_interpolation_custom_loader(config, config_file):
    config.option.from_yaml(config_file, loader=yaml.UnsafeLoader)

    assert config.option.section1() == {
        "value1": "test-value",
        "value2": "test-path/path",
    }
    assert config.option.section1.value1() == "test-value"
    assert config.option.section1.value2() == "test-path/path"
