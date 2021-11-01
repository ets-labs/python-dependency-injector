"""Tests for configuration provider linking."""


from dependency_injector import containers, providers


class Core(containers.DeclarativeContainer):
    config = providers.Configuration("core")
    value_getter = providers.Callable(lambda _: _, config.value)


class Services(containers.DeclarativeContainer):
    config = providers.Configuration("services")
    value_getter = providers.Callable(lambda _: _, config.value)


def test():
    root_config = providers.Configuration("main")
    core = Core(config=root_config.core)
    services = Services(config=root_config.services)

    root_config.override(
        {
            "core": {
                "value": "core",
            },
            "services": {
                "value": "services",
            },
        },
    )

    assert core.config() == {"value": "core"}
    assert core.config.value() == "core"
    assert core.value_getter() == "core"

    assert services.config() == {"value": "services"}
    assert services.config.value() == "services"
    assert services.value_getter() == "services"


def test_double_override():
    root_config = providers.Configuration("main")
    core = Core(config=root_config.core)
    services = Services(config=root_config.services)

    root_config.override(
        {
            "core": {
                "value": "core1",
            },
            "services": {
                "value": "services1",
            },
        },
    )
    root_config.override(
        {
            "core": {
                "value": "core2",
            },
            "services": {
                "value": "services2",
            },
        },
    )

    assert core.config() == {"value": "core2"}
    assert core.config.value() == "core2"
    assert core.value_getter() == "core2"

    assert services.config() == {"value": "services2"}
    assert services.config.value() == "services2"
    assert services.value_getter() == "services2"


def test_reset_overriding_cache():
    # See: https://github.com/ets-labs/python-dependency-injector/issues/428
    class Core(containers.DeclarativeContainer):
        config = providers.Configuration()

        greetings = providers.Factory(str, config.greeting)

    class Application(containers.DeclarativeContainer):
        config = providers.Configuration()

        core = providers.Container(
            Core,
            config=config,
        )

        greetings = providers.Factory(str, config.greeting)

    container = Application()

    container.config.set("greeting", "Hello World")
    assert container.greetings() == "Hello World"
    assert container.core.greetings() == "Hello World"

    container.config.set("greeting", "Hello Bob")
    assert container.greetings() == "Hello Bob"
    assert container.core.greetings() == "Hello Bob"


def test_reset_overriding_cache_for_option():
    # See: https://github.com/ets-labs/python-dependency-injector/issues/428
    class Core(containers.DeclarativeContainer):
        config = providers.Configuration()

        greetings = providers.Factory(str, config.greeting)

    class Application(containers.DeclarativeContainer):
        config = providers.Configuration()

        core = providers.Container(
            Core,
            config=config.option,
        )

        greetings = providers.Factory(str, config.option.greeting)

    container = Application()

    container.config.set("option.greeting", "Hello World")
    assert container.greetings() == "Hello World"
    assert container.core.greetings() == "Hello World"

    container.config.set("option.greeting", "Hello Bob")
    assert container.greetings() == "Hello Bob"
    assert container.core.greetings() == "Hello Bob"
