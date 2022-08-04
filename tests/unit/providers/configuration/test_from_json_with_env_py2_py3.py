"""Configuration.from_json() with environment variables interpolation tests."""

import json
import os

from pytest import mark, raises


def test_env_variable_interpolation(config, json_config_file_3):
    config.from_json(json_config_file_3)

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


def test_missing_envs_not_required(config, json_config_file_3):
    del os.environ["CONFIG_TEST_ENV"]
    del os.environ["CONFIG_TEST_PATH"]

    config.from_json(json_config_file_3)

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


def test_missing_envs_required(config, json_config_file_3):
    with open(json_config_file_3, "w") as file:
        file.write(
            json.dumps(
                {
                    "section": {
                        "undefined": "${UNDEFINED}",
                    },
                },
            ),
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.from_json(json_config_file_3, envs_required=True)


@mark.parametrize("config_type", ["strict"])
def test_missing_envs_strict_mode(config, json_config_file_3):
    with open(json_config_file_3, "w") as file:
        file.write(
            json.dumps(
                {
                    "section": {
                        "undefined": "${UNDEFINED}",
                    },
                },
            ),
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.from_json(json_config_file_3)


@mark.parametrize("config_type", ["strict"])
def test_missing_envs_not_required_in_strict_mode(config, json_config_file_3):
    with open(json_config_file_3, "w") as file:
        file.write(
            json.dumps(
                {
                    "section": {
                        "undefined": "${UNDEFINED}",
                    },
                },
            ),
        )
    config.from_json(json_config_file_3, envs_required=False)
    assert config.section.undefined() == ""


def test_option_missing_envs_not_required(config, json_config_file_3):
    del os.environ["CONFIG_TEST_ENV"]
    del os.environ["CONFIG_TEST_PATH"]

    config.option.from_json(json_config_file_3)

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


def test_option_missing_envs_required(config, json_config_file_3):
    with open(json_config_file_3, "w") as file:
        file.write(
            json.dumps(
                {
                    "section": {
                        "undefined": "${UNDEFINED}",
                    },
                },
            ),
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.option.from_json(json_config_file_3, envs_required=True)


@mark.parametrize("config_type", ["strict"])
def test_option_missing_envs_not_required_in_strict_mode(config, json_config_file_3):
    config.override({"option": {}})
    with open(json_config_file_3, "w") as file:
        file.write(
            json.dumps(
                {
                    "section": {
                        "undefined": "${UNDEFINED}",
                    },
                },
            ),
        )
    config.option.from_json(json_config_file_3, envs_required=False)
    assert config.option.section.undefined() == ""


@mark.parametrize("config_type", ["strict"])
def test_option_missing_envs_strict_mode(config, json_config_file_3):
    with open(json_config_file_3, "w") as file:
        file.write(
            json.dumps(
                {
                    "section": {
                        "undefined": "${UNDEFINED}",
                    },
                },
            ),
        )
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.option.from_json(json_config_file_3)


def test_default_values(config, json_config_file_3):
    with open(json_config_file_3, "w") as file:
        file.write(
            json.dumps(
                {
                    "section": {
                        "defined_with_default": "${DEFINED:default}",
                        "undefined_with_default": "${UNDEFINED:default}",
                        "complex": "${DEFINED}/path/${DEFINED:default}/${UNDEFINED}/${UNDEFINED:default}",
                    },
                },
            ),
        )

    config.from_json(json_config_file_3)

    assert config.section() == {
        "defined_with_default": "defined",
        "undefined_with_default": "default",
        "complex": "defined/path/defined//default",
    }


def test_option_env_variable_interpolation(config, json_config_file_3):
    config.option.from_json(json_config_file_3)

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
