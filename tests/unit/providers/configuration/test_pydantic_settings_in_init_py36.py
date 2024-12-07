"""Configuration.from_pydantic() tests."""

from pydantic import BaseModel

try:
    from pydantic_settings import (
        BaseSettings,  # type: ignore[import-not-found,unused-ignore]
    )
except ImportError:
    try:
        from pydantic import BaseSettings  # type: ignore[no-redef,unused-ignore]
    except ImportError:

        class BaseSettings:  # type: ignore[no-redef]
            """No-op fallback"""


from pytest import fixture, mark, raises

from dependency_injector import providers

pytestmark = mark.pydantic


class Section11(BaseModel):
    value1: int = 1


class Section12(BaseModel):
    value2: int = 2


class Settings1(BaseSettings):
    section1: Section11 = Section11()
    section2: Section12 = Section12()


class Section21(BaseModel):
    value1: int = 11
    value11: int = 11


class Section3(BaseModel):
    value3: int = 3


class Settings2(BaseSettings):
    section1: Section21 = Section21()
    section3: Section3 = Section3()


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
    class Settings3(BaseSettings):
        ...

    class Settings4(BaseSettings):
        ...

    settings_3 = Settings3()
    settings_4 = Settings4()

    config.set_pydantic_settings([settings_3, settings_4])
    assert config.get_pydantic_settings() == [settings_3, settings_4]


def test_file_does_not_exist(config):
    config.set_pydantic_settings([BaseSettings()])
    config.load()
    assert config() == {}


@mark.parametrize("config_type", ["strict"])
def test_file_does_not_exist_strict_mode(config):
    config.set_pydantic_settings([BaseSettings()])
    with raises(ValueError):
        config.load()
    assert config() == {}


def test_required_file_does_not_exist(config):
    config.set_pydantic_settings([BaseSettings()])
    with raises(ValueError):
        config.load(required=True)


@mark.parametrize("config_type", ["strict"])
def test_not_required_file_does_not_exist_strict_mode(config):
    config.set_pydantic_settings([BaseSettings()])
    config.load(required=False)
    assert config() == {}
