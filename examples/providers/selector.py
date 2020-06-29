"""`Selector` provider example."""

from dependency_injector import providers


class SomeClass:
    ...


class SomeOtherClass:
    ...


config = providers.Configuration()

selector = providers.Selector(
    config.one_or_another,
    one=providers.Factory(SomeClass),
    another=providers.Factory(SomeOtherClass),
)

config.override({'one_or_another': 'one'})
some_instance_1 = selector()
assert isinstance(some_instance_1, SomeClass)

config.override({'one_or_another': 'another'})
some_instance_2 = selector()
assert isinstance(some_instance_2, SomeOtherClass)
