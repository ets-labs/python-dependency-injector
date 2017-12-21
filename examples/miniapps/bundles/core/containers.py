"""Containers module."""

import six

from dependency_injector import containers

from core import providers


class DeclarativeContainer(containers.DeclarativeContainer):
    """Declarative container."""

    def __new__(cls, **dependencies):
        """Constructor.

        :return: Dynamic container with copy of all providers.
        :rtype: :py:class:`DynamicContainer`
        """
        # Make copy of declarative container providers for container instance
        container_providers = providers.deepcopy(cls.providers)

        # Fetch container dependencies
        container_dependencies = dict()
        for name, provider in six.iteritems(container_providers):
            if isinstance(provider, providers.Dependency):
                container_dependencies[name] = provider

        # Satisfy container dependencies
        for name, dependency in six.iteritems(container_dependencies):
            try:
                dependency_provider = dependencies[name]
            except KeyError:
                raise Exception('Dependency {name} of container {container} '
                                'is not satisfied'.format(
                                    name=name, container=cls))
            else:
                dependency.provided_by(dependency_provider)

        # Create dynamic container
        container = cls.instance_type()
        container.provider_type = cls.provider_type
        for name, provider in six.iteritems(container_providers):
            setattr(container, name, provider)

        return container
