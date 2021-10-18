"""Configuration provider tests."""

from dependency_injector import providers


def test_traverse():
    config = providers.Configuration(default={"option1": {"option2": "option2"}})
    option1 = config.option1
    option2 = config.option1.option2
    option3 = config.option1[config.option1.option2]

    all_providers = list(config.traverse())

    assert len(all_providers) == 3
    assert option1 in all_providers
    assert option2 in all_providers
    assert option3 in all_providers


def test_traverse_typed():
    config = providers.Configuration()
    option = config.option
    typed_option = config.option.as_int()

    all_providers = list(typed_option.traverse())

    assert len(all_providers) == 1
    assert option in all_providers


def test_traverse_overridden():
    options = {"option1": {"option2": "option2"}}
    config = providers.Configuration()
    config.from_dict(options)

    all_providers = list(config.traverse())

    assert len(all_providers) == 1
    overridden, = all_providers
    assert overridden() == options
    assert overridden is config.last_overriding


def test_traverse_overridden_option_1():
    options = {"option2": "option2"}
    config = providers.Configuration()
    config.option1.from_dict(options)

    all_providers = list(config.traverse())

    assert len(all_providers) == 2
    assert config.option1 in all_providers
    assert config.last_overriding in all_providers


def test_traverse_overridden_option_2():
    options = {"option2": "option2"}
    config = providers.Configuration()
    config.option1.from_dict(options)

    all_providers = list(config.option1.traverse())

    assert len(all_providers) == 0
