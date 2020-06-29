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
instance_1 = selector()
assert isinstance(instance_1, SomeClass)

config.override({'one_or_another': 'another'})
instance_2 = selector()
assert isinstance(instance_2, SomeOtherClass)
