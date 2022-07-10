"""Configuration.from_pydantic() tests."""

import pydantic
from dependency_injector import providers
from pytest import fixture, mark, raises


class Section11(pydantic.BaseModel):
    value1 = 1


class Section12(pydantic.BaseModel):
    value2 = 2


class Settings1(pydantic.BaseSettings):
    section1 = Section11()
    section2 = Section12()


class Section21(pydantic.BaseModel):
    value1 = 11
    value11 = 11


class Section3(pydantic.BaseModel):
    value3 = 3


class Settings2(pydantic.BaseSettings):
    section1 = Section21()
    section3 = Section3()


@fixture
def config(config_type, pydantic_settings_1, pydantic_settings_2):
    if config_type == "strict":
        return providers.Configuration(strict=True)
    elif config_type == "default":
        return providers.Configuration(pydantic_settings=[pydantic_settings_1, pydantic_settings_2])
    else:
        raise ValueError("Undefined config type \"{0}\"".format(config_type))


@fixture
def pydantic_settings_1():
    return Settings1()


@fixture
def pydantic_settings_2():
    return Settings2()


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


def test_get_pydantic_settings(config, pydantic_settings_1, pydantic_settings_2):
    assert config.get_pydantic_settings() == [pydantic_settings_1, pydantic_settings_2]


def test_copy(config, pydantic_settings_1, pydantic_settings_2):
    config_copy = providers.deepcopy(config)
    assert config_copy.get_pydantic_settings() == [pydantic_settings_1, pydantic_settings_2]


def test_set_pydantic_settings(config):
    class Settings3(pydantic.BaseSettings):
        ...

    class Settings4(pydantic.BaseSettings):
        ...

    settings_3 = Settings3()
    settings_4 = Settings4()

    config.set_pydantic_settings([settings_3, settings_4])
    assert config.get_pydantic_settings() == [settings_3, settings_4]


def test_file_does_not_exist(config):
    config.set_pydantic_settings([pydantic.BaseSettings()])
    config.load()
    assert config() == {}


@mark.parametrize("config_type", ["strict"])
def test_file_does_not_exist_strict_mode(config):
    config.set_pydantic_settings([pydantic.BaseSettings()])
    with raises(ValueError):
        config.load()
    assert config() == {}


def test_required_file_does_not_exist(config):
    config.set_pydantic_settings([pydantic.BaseSettings()])
    with raises(ValueError):
        config.load(required=True)


@mark.parametrize("config_type", ["strict"])
def test_not_required_file_does_not_exist_strict_mode(config):
    config.set_pydantic_settings([pydantic.BaseSettings()])
    config.load(required=False)
    assert config() == {}
