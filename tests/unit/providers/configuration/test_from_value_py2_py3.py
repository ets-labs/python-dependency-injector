"""Configuration.from_value() tests."""


def test_from_value(config):
    test_value = 123321
    config.from_value(test_value)
    assert config() == test_value


def test_option_from_value(config):
    test_value_1 = 123
    test_value_2 = 321

    config.option1.from_value(test_value_1)
    config.option2.from_value(test_value_2)

    assert config() == {"option1": test_value_1, "option2": test_value_2}
    assert config.option1() == test_value_1
    assert config.option2() == test_value_2
