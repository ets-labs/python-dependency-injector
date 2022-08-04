"""Configuration(yaml_files=[...]) tests."""

from dependency_injector import providers
from pytest import fixture, mark, raises


@fixture
def config(config_type, yaml_config_file_1, yaml_config_file_2):
    if config_type == "strict":
        return providers.Configuration(strict=True)
    elif config_type == "default":
        return providers.Configuration(yaml_files=[yaml_config_file_1, yaml_config_file_2])
    else:
        raise ValueError("Undefined config type \"{0}\"".format(config_type))


def test_load(config):
    config.load()

    assert config() == {
        "section1": {
            "value1": 11,
            "value11": 11,
        },
        "section2": {
            "value2": 2,
        },
        "section3": {
            "value3": 3,
        },
    }
    assert config.section1() == {"value1": 11, "value11": 11}
    assert config.section1.value1() == 11
    assert config.section1.value11() == 11
    assert config.section2() == {"value2": 2}
    assert config.section2.value2() == 2
    assert config.section3() == {"value3": 3}
    assert config.section3.value3() == 3


def test_get_files(config, yaml_config_file_1, yaml_config_file_2):
    assert config.get_yaml_files() == [yaml_config_file_1, yaml_config_file_2]


def test_set_files(config):
    config.set_yaml_files(["file1.yml", "file2.yml"])
    assert config.get_yaml_files() == ["file1.yml", "file2.yml"]


def test_copy(config, yaml_config_file_1, yaml_config_file_2):
    config_copy = providers.deepcopy(config)
    assert config_copy.get_yaml_files() == [yaml_config_file_1, yaml_config_file_2]


def test_file_does_not_exist(config):
    config.set_yaml_files(["./does_not_exist.yml"])
    config.load()
    assert config() == {}


@mark.parametrize("config_type", ["strict"])
def test_file_does_not_exist_strict_mode(config):
    config.set_yaml_files(["./does_not_exist.yml"])
    with raises(IOError):
        config.load()
    assert config() == {}


def test_required_file_does_not_exist(config):
    config.set_yaml_files(["./does_not_exist.yml"])
    with raises(IOError):
        config.load(required=True)


@mark.parametrize("config_type", ["strict"])
def test_not_required_file_does_not_exist_strict_mode(config):
    config.set_yaml_files(["./does_not_exist.yml"])
    config.load(required=False)
    assert config() == {}


def test_missing_envs_required(config, yaml_config_file_3):
    with open(yaml_config_file_3, "w") as file:
        file.write(
            "section:\n"
            "  undefined: ${UNDEFINED}\n"
        )
    config.set_yaml_files([yaml_config_file_3])
    with raises(ValueError, match="Missing required environment variable \"UNDEFINED\""):
        config.load(envs_required=True)


@mark.parametrize("config_type", ["strict"])
def test_missing_envs_not_required_in_strict_mode(config, yaml_config_file_3):
    with open(yaml_config_file_3, "w") as file:
        file.write(
            "section:\n"
            "  undefined: ${UNDEFINED}\n"
        )
    config.set_yaml_files([yaml_config_file_3])
    config.load(envs_required=False)
    assert config.section.undefined() is None
