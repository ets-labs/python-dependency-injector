"""`DelegatedCallable` providers example."""

from dependency_injector import providers


def command1(config):
    """Some example command."""
    return config['some_value'] * 5


def command2(command1):
    """Some example command."""
    return command1() / 2

# Creating callable providers for commands:
command1_provider = providers.DelegatedCallable(command1,
                                                config={'some_value': 4})
command2_provider = providers.DelegatedCallable(command2,
                                                command1=command1_provider)

# Making some asserts:
assert command2_provider() == 10
