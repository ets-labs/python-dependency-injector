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

from dependency_injector import errors, providers

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
def no_pydantic_module_installed():
    has_pydantic_settings = providers.has_pydantic_settings
    providers.has_pydantic_settings = False
    yield
    providers.has_pydantic_settings = has_pydantic_settings


def test(config):
    config.from_pydantic(Settings1())

    assert config() == {"section1": {"value1": 1}, "section2": {"value2": 2}}
    assert config.section1() == {"value1": 1}
    assert config.section1.value1() == 1
    assert config.section2() == {"value2": 2}
    assert config.section2.value2() == 2


def test_kwarg(config):
    config.from_pydantic(Settings1(), exclude={"section2"})

    assert config() == {"section1": {"value1": 1}}
    assert config.section1() == {"value1": 1}
    assert config.section1.value1() == 1


def test_merge(config):
    config.from_pydantic(Settings1())
    config.from_pydantic(Settings2())

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


def test_empty_settings(config):
    config.from_pydantic(BaseSettings())
    assert config() == {}


@mark.parametrize("config_type", ["strict"])
def test_empty_settings_strict_mode(config):
    with raises(ValueError):
        config.from_pydantic(BaseSettings())


def test_option_empty_settings(config):
    config.option.from_pydantic(BaseSettings())
    assert config.option() == {}


@mark.parametrize("config_type", ["strict"])
def test_option_empty_settings_strict_mode(config):
    with raises(ValueError):
        config.option.from_pydantic(BaseSettings())


def test_required_empty_settings(config):
    with raises(ValueError):
        config.from_pydantic(BaseSettings(), required=True)


def test_required_option_empty_settings(config):
    with raises(ValueError):
        config.option.from_pydantic(BaseSettings(), required=True)


@mark.parametrize("config_type", ["strict"])
def test_not_required_empty_settings_strict_mode(config):
    config.from_pydantic(BaseSettings(), required=False)
    assert config() == {}


@mark.parametrize("config_type", ["strict"])
def test_not_required_option_empty_settings_strict_mode(config):
    config.option.from_pydantic(BaseSettings(), required=False)
    assert config.option() == {}
    assert config() == {"option": {}}


def test_not_instance_of_settings(config):
    with raises(
        errors.Error,
        match=(
            r"Unable to recognize settings instance, expect \"pydantic(?:_settings)?\.BaseSettings\", "
            r"got {0} instead".format({})
        ),
    ):
        config.from_pydantic({})


def test_option_not_instance_of_settings(config):
    with raises(
        errors.Error,
        match=(
            r"Unable to recognize settings instance, expect \"pydantic(?:_settings)?\.BaseSettings\", "
            "got {0} instead".format({})
        ),
    ):
        config.option.from_pydantic({})


def test_subclass_instead_of_instance(config):
    with raises(errors.Error) as error:
        config.from_pydantic(Settings1)
    assert error.value.args[0] == (
        "Got settings class, but expect instance: "
        "instead \"Settings1\" use \"Settings1()\""
    )


def test_option_subclass_instead_of_instance(config):
    with raises(errors.Error) as error:
        config.option.from_pydantic(Settings1)
    assert error.value.args[0] == (
        "Got settings class, but expect instance: "
        "instead \"Settings1\" use \"Settings1()\""
    )


@mark.usefixtures("no_pydantic_module_installed")
def test_no_pydantic_installed(config):
    with raises(
        errors.Error,
        match=(
            r"Unable to load pydantic configuration - pydantic(?:_settings)? is not installed\. "
            r"Install pydantic or install Dependency Injector with pydantic extras: "
            r"\"pip install dependency-injector\[pydantic2?\]\""
        ),
    ):
        config.from_pydantic(Settings1())


@mark.usefixtures("no_pydantic_module_installed")
def test_option_no_pydantic_installed(config):
    with raises(
        errors.Error,
        match=(
            r"Unable to load pydantic configuration - pydantic(?:_settings)? is not installed\. "
            r"Install pydantic or install Dependency Injector with pydantic extras: "
            r"\"pip install dependency-injector\[pydantic2?\]\""
        ),
    ):
        config.option.from_pydantic(Settings1())
