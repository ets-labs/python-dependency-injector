"""Configuration.from_dict() tests."""

from pytest import mark, raises


CONFIG_OPTIONS_1 = {
    "section1": {
        "value1": "1",
    },
    "section2": {
        "value2": "2",
    },
}
CONFIG_OPTIONS_2 = {
    "section1": {
        "value1": "11",
        "value11": "11",
    },
    "section3": {
        "value3": "3",
    },
}


def test(config):
    config.from_dict(CONFIG_OPTIONS_1)

    assert config() == {"section1": {"value1": "1"}, "section2": {"value2": "2"}}
    assert config.section1() == {"value1": "1"}
    assert config.section1.value1() == "1"
    assert config.section2() == {"value2": "2"}
    assert config.section2.value2() == "2"


def test_merge(config):
    config.from_dict(CONFIG_OPTIONS_1)
    config.from_dict(CONFIG_OPTIONS_2)

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


def test_empty_dict(config):
    config.from_dict({})
    assert config() == {}


def test_option_empty_dict(config):
    config.option.from_dict({})
    assert config.option() == {}


@mark.parametrize("config_type", ["strict"])
def test_empty_dict_in_strict_mode(config):
    with raises(ValueError):
        config.from_dict({})


@mark.parametrize("config_type", ["strict"])
def test_option_empty_dict_in_strict_mode(config):
    with raises(ValueError):
        config.option.from_dict({})


def test_required_empty_dict(config):
    with raises(ValueError):
        config.from_dict({}, required=True)


def test_required_option_empty_dict(config):
    with raises(ValueError):
        config.option.from_dict({}, required=True)


@mark.parametrize("config_type", ["strict"])
def test_not_required_empty_dict_strict_mode(config):
    config.from_dict({}, required=False)
    assert config() == {}


@mark.parametrize("config_type", ["strict"])
def test_not_required_option_empty_dict_strict_mode(config):
    config.option.from_dict({}, required=False)
    assert config.option() == {}
    assert config() == {"option": {}}

