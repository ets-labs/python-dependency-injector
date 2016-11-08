"""Dependency injector container utils."""


import six

from dependency_injector.providers import deepcopy
from dependency_injector.errors import Error


def is_container(instance):
    """Check if instance is container instance.

    :param instance: Instance to be checked.
    :type instance: object

    :rtype: bool
    """
    return getattr(instance, '__IS_CONTAINER__', False) is True


def override(container):
    """:py:class:`DeclarativeContainer` overriding decorator.

    :param container: Container that should be overridden by decorated
                      container.
    :type container: :py:class:`DeclarativeContainer`

    :return: Declarative container's overriding decorator.
    :rtype: callable(:py:class:`DeclarativeContainer`)
    """
    def _decorator(overriding_container):
        """Overriding decorator."""
        container.override(overriding_container)
        return overriding_container
    return _decorator


def copy(container):
    """:py:class:`DeclarativeContainer` copying decorator.

    This decorator copy all providers from provided container to decorated one.
    If one of the decorated container providers matches to source container
    providers by name, it would be replaced by reference.

    :param container: Container that should be copied by decorated container.
    :type container: :py:class:`DeclarativeContainer`

    :return: Declarative container's copying decorator.
    :rtype: callable(:py:class:`DeclarativeContainer`)
    """
    def _decorator(copied_container):
        memo = dict()
        for name, provider in six.iteritems(copied_container.cls_providers):
            try:
                source_provider = getattr(container, name)
            except AttributeError:
                pass
            else:
                memo[id(source_provider)] = provider

        providers_copy = deepcopy(container.providers, memo)
        for name, provider in six.iteritems(providers_copy):
            setattr(copied_container, name, provider)

        return copied_container
    return _decorator


def _check_provider_type(cls, provider):
    if not isinstance(provider, cls.provider_type):
        raise Error('{0} can contain only {1} '
                    'instances'.format(cls, cls.provider_type))
