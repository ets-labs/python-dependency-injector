"""Fixtures module."""

from dependency_injector import providers
from pytest import fixture


@fixture
def config_type():
    return "default"


@fixture
def config(config_type):
    if config_type == "strict":
        return providers.Configuration(strict=True)
    elif config_type == "default":
        return providers.Configuration()
    else:
        raise ValueError("Undefined config type \"{0}\"".format(config_type))


@fixture
def yaml_config_file_1(tmp_path):
    config_file = str(tmp_path / "config_1.yml")
    with open(config_file, "w") as file:
        file.write(
            "section1:\n"
            "  value1: 1\n"
            "\n"
            "section2:\n"
            "  value2: 2\n"
        )
    return config_file


@fixture
def yaml_config_file_2(tmp_path):
    config_file = str(tmp_path / "config_2.yml")
    with open(config_file, "w") as file:
        file.write(
            "section1:\n"
            "  value1: 11\n"
            "  value11: 11\n"
            "section3:\n"
            "  value3: 3\n"
        )
    return config_file


@fixture
def yaml_config_file_3(tmp_path):
    yaml_config_file_3 = str(tmp_path / "config_1.yml")
    with open(yaml_config_file_3, "w") as file:
        file.write(
            "section1:\n"
            "  value1: ${CONFIG_TEST_ENV}\n"
            "  value2: ${CONFIG_TEST_PATH}/path\n"
        )
    return yaml_config_file_3
