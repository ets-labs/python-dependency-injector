"""Providers module."""

from dependency_injector import providers


Factory = providers.Factory
Singleton = providers.Singleton


deepcopy = providers.deepcopy


class Dependency(providers.ExternalDependency):
    """Dependency provider."""

    def __init__(self, type=object):
        """Initializer."""
        super(Dependency, self).__init__(type)
