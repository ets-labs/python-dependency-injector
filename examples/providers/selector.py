"""`Selector` provider example."""

from dependency_injector import containers, providers


class SomeClass:
    ...


class SomeOtherClass:
    ...


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    selector = providers.Selector(
        config.one_or_another,
        one=providers.Factory(SomeClass),
        another=providers.Factory(SomeOtherClass),
    )


if __name__ == "__main__":
    container = Container()

    container.config.override({"one_or_another": "one"})
    instance_1 = container.selector()
    assert isinstance(instance_1, SomeClass)

    container.config.override({"one_or_another": "another"})
    instance_2 = container.selector()
    assert isinstance(instance_2, SomeOtherClass)
