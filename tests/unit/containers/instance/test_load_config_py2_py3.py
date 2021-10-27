"""Tests for container config loading."""

from dependency_injector import containers, providers
from pytest import fixture


@fixture
def yaml_config_file(tmp_path):
    config_file = str(tmp_path / "config.yml")
    with open(config_file, "w") as file:
        file.write(
            "section1:\n"
            "  value1: yaml-loaded\n"
        )
    return config_file


@fixture
def ini_config_file(tmp_path):
    config_file = str(tmp_path / "config.ini")
    with open(config_file, "w") as file:
        file.write(
            "[section2]:\n"
            "value2 = ini-loaded\n"
        )
    return config_file



def test_auto_load(yaml_config_file, ini_config_file):
    class ContainerWithConfig(containers.DeclarativeContainer):
        config = providers.Configuration(
            yaml_files=[yaml_config_file],
            ini_files=[ini_config_file],
        )

    container = ContainerWithConfig()
    assert container.config.section1.value1() == "yaml-loaded"
    assert container.config.section2.value2() == "ini-loaded"


def test_auto_load_and_overriding(yaml_config_file):
    class ContainerWithConfig(containers.DeclarativeContainer):
        config = providers.Configuration(yaml_files=[yaml_config_file])

    container = ContainerWithConfig(config={"section1": {"value1": "overridden"}})
    assert container.config.section1.value1() == "overridden"


def test_manual_load(yaml_config_file):
    class ContainerWithConfig(containers.DeclarativeContainer):
        auto_load_config = False
        config = providers.Configuration(yaml_files=[yaml_config_file])

    container = ContainerWithConfig()
    assert container.config.section1.value1() is None

    container.load_config()
    assert container.config.section1.value1() == "yaml-loaded"


def test_load_config_does_not_affect_class(yaml_config_file):
    class ContainerWithConfig(containers.DeclarativeContainer):
        config = providers.Configuration(yaml_files=[yaml_config_file])

    assert ContainerWithConfig.config.section1.value1() is None
    _ = ContainerWithConfig()
    assert ContainerWithConfig.config.section1.value1() is None
