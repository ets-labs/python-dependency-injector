"""Configuration.from_ini() tests."""

from dependency_injector import errors
from pytest import fixture, mark, raises


@fixture
def config_file_1(tmp_path):
    config_file = str(tmp_path / "config_1.ini")
    with open(config_file, "w") as file:
        file.write(
            "[section1]\n"
            "value1=1\n"
            "\n"
            "[section2]\n"
            "value2=2\n"
        )
    return config_file


@fixture
def config_file_2(tmp_path):
    config_file = str(tmp_path / "config_2.ini")
    with open(config_file, "w") as file:
        file.write(
            "[section1]\n"
            "value1=11\n"
            "value11=11\n"
            "[section3]\n"
            "value3=3\n"
        )
    return config_file


def test(config, config_file_1):
    config.from_ini(config_file_1)

    assert config() == {"section1": {"value1": "1"}, "section2": {"value2": "2"}}
    assert config.section1() == {"value1": "1"}
    assert config.section1.value1() == "1"
    assert config.section2() == {"value2": "2"}
    assert config.section2.value2() == "2"


def test_option(config, config_file_1):
    config.option.from_ini(config_file_1)

    assert config() == {"option": {"section1": {"value1": "1"}, "section2": {"value2": "2"}}}
    assert config.option() == {"section1": {"value1": "1"}, "section2": {"value2": "2"}}
    assert config.option.section1() == {"value1": "1"}
    assert config.option.section1.value1() == "1"
    assert config.option.section2() == {"value2": "2"}
    assert config.option.section2.value2() == "2"


def test_merge(config, config_file_1, config_file_2):
    config.from_ini(config_file_1)
    config.from_ini(config_file_2)

    assert config() == {
        "section1": {
            "value1": "11",
            "value11": "11",
        },
        "section2": {
            "value2": "2",
        },
        "section3": {
            "value3": "3",
        },
    }
    assert config.section1() == {"value1": "11", "value11": "11"}
    assert config.section1.value1() == "11"
    assert config.section1.value11() == "11"
    assert config.section2() == {"value2": "2"}
    assert config.section2.value2() == "2"
    assert config.section3() == {"value3": "3"}
    assert config.section3.value3() == "3"


def test_file_does_not_exist(config):
    config.from_ini("./does_not_exist.ini")
    assert config() == {}


@mark.parametrize("config_type", ["strict"])
def test_file_does_not_exist_strict_mode(config):
    with raises(IOError):
        config.from_ini("./does_not_exist.ini")


def test_option_file_does_not_exist(config):
    config.option.from_ini("does_not_exist.ini")
    assert config.option.undefined() is None


@mark.parametrize("config_type", ["strict"])
def test_option_file_does_not_exist_strict_mode(config):
    with raises(IOError):
        config.option.from_ini("./does_not_exist.ini")


def test_required_file_does_not_exist(config):
    with raises(IOError):
        config.from_ini("./does_not_exist.ini", required=True)


def test_required_option_file_does_not_exist(config):
    with raises(IOError):
        config.option.from_ini("./does_not_exist.ini", required=True)


@mark.parametrize("config_type", ["strict"])
def test_not_required_file_does_not_exist_strict_mode(config):
    config.from_ini("./does_not_exist.ini", required=False)
    assert config() == {}


@mark.parametrize("config_type", ["strict"])
def test_not_required_option_file_does_not_exist_strict_mode(config):
    config.option.from_ini("./does_not_exist.ini", required=False)
    with raises(errors.Error):
        config.option()
