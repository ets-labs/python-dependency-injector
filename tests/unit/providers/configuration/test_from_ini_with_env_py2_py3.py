"""Configuration.from_ini() with environment variables interpolation tests."""

import os

from pytest import mark, raises


def test_env_variable_interpolation(config, ini_config_file_3):
    config.from_ini(ini_config_file_3)

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


def test_missing_envs_not_required(config, ini_config_file_3):
    del os.environ["CONFIG_TEST_ENV"]
    del os.environ["CONFIG_TEST_PATH"]

    config.from_ini(ini_config_file_3)

    assert config() == {
        "section1": {
            "value1": "",
            "value2": "/path",
        },
    }
    assert config.section1() == {
        "value1": "",
        "value2": "/path",
    }
    assert config.section1.value1() == ""
    assert config.section1.value2() == "/path"


def test_missing_envs_required(config, ini_config_file_3):
    with open(ini_config_file_3, "w") as file:
        file.write(
            "[section]\n"
            "undefined=${UNDEFINED}\n"
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.from_ini(ini_config_file_3, envs_required=True)


@mark.parametrize("config_type", ["strict"])
def test_missing_envs_strict_mode(config, ini_config_file_3):
    with open(ini_config_file_3, "w") as file:
        file.write(
            "[section]\n"
            "undefined=${UNDEFINED}\n"
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.from_ini(ini_config_file_3)


@mark.parametrize("config_type", ["strict"])
def test_missing_envs_not_required_in_strict_mode(config, ini_config_file_3):
    with open(ini_config_file_3, "w") as file:
        file.write(
            "[section]\n"
            "undefined=${UNDEFINED}\n"
        )
    config.from_ini(ini_config_file_3, envs_required=False)
    assert config.section.undefined() == ""


def test_option_missing_envs_not_required(config, ini_config_file_3):
    del os.environ["CONFIG_TEST_ENV"]
    del os.environ["CONFIG_TEST_PATH"]

    config.option.from_ini(ini_config_file_3)

    assert config.option() == {
        "section1": {
            "value1": "",
            "value2": "/path",
        },
    }
    assert config.option.section1() == {
        "value1": "",
        "value2": "/path",
    }
    assert config.option.section1.value1() == ""
    assert config.option.section1.value2() == "/path"


def test_option_missing_envs_required(config, ini_config_file_3):
    with open(ini_config_file_3, "w") as file:
        file.write(
            "[section]\n"
            "undefined=${UNDEFINED}\n"
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.option.from_ini(ini_config_file_3, envs_required=True)


@mark.parametrize("config_type", ["strict"])
def test_option_missing_envs_not_required_in_strict_mode(config, ini_config_file_3):
    config.override({"option": {}})
    with open(ini_config_file_3, "w") as file:
        file.write(
            "[section]\n"
            "undefined=${UNDEFINED}\n"
        )
    config.option.from_ini(ini_config_file_3, envs_required=False)
    assert config.option.section.undefined() == ""


@mark.parametrize("config_type", ["strict"])
def test_option_missing_envs_strict_mode(config, ini_config_file_3):
    with open(ini_config_file_3, "w") as file:
        file.write(
            "[section]\n"
            "undefined=${UNDEFINED}\n"
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.option.from_ini(ini_config_file_3)


def test_default_values(config, ini_config_file_3):
    with open(ini_config_file_3, "w") as file:
        file.write(
            "[section]\n"
            "defined_with_default=${DEFINED:default}\n"
            "undefined_with_default=${UNDEFINED:default}\n"
            "complex=${DEFINED}/path/${DEFINED:default}/${UNDEFINED}/${UNDEFINED:default}\n"
        )

    config.from_ini(ini_config_file_3)

    assert config.section() == {
        "defined_with_default": "defined",
        "undefined_with_default": "default",
        "complex": "defined/path/defined//default",
    }
