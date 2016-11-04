"""Dependency injector dynamic container."""

import six

from dependency_injector.providers import Provider
from dependency_injector.errors import Error

from .utils import _check_provider_type


class DynamicContainer(object):
    """Dynamic inversion of control container.

    .. code-block:: python

        services = DynamicContainer()
        services.auth = providers.Factory(AuthService)
        services.users = providers.Factory(UsersService,
                                           auth_service=services.auth)

    .. py:attribute:: providers

        Read-only dictionary of all providers.

        :type: dict[str, :py:class:`dependency_injector.providers.Provider`]

    .. py:attribute:: overridden

        Tuple of overriding containers.

        :type: tuple[:py:class:`DynamicContainer`]

    .. py:attribute:: provider_type

        Type of providers that could be placed in container.

        :type: type
    """

    __IS_CONTAINER__ = True

    def __init__(self):
        """Initializer.

        :rtype: None
        """
        self.provider_type = Provider
        self.providers = dict()
        self.overridden = tuple()
        super(DynamicContainer, self).__init__()

    def __setattr__(self, name, value):
        """Set instance attribute.

        If value of attribute is provider, it will be added into providers
        dictionary.

        :param name: Attribute's name
        :type name: str

        :param value: Attribute's value
        :type value: object

        :rtype: None
        """
        if isinstance(value, Provider):
            _check_provider_type(self, value)
            self.providers[name] = value
        super(DynamicContainer, self).__setattr__(name, value)

    def __delattr__(self, name):
        """Delete instance attribute.

        If value of attribute is provider, it will be deleted from providers
        dictionary.

        :param name: Attribute's name
        :type name: str

        :rtype: None
        """
        if name in self.providers:
            del self.providers[name]
        super(DynamicContainer, self).__delattr__(name)

    def override(self, overriding):
        """Override current container by overriding container.

        :param overriding: Overriding container.
        :type overriding: :py:class:`DynamicContainer`

        :raise: :py:exc:`dependency_injector.errors.Error` if trying to
                override container by itself

        :rtype: None
        """
        if overriding is self:
            raise Error('Container {0} could not be overridden '
                        'with itself'.format(self))

        self.overridden += (overriding,)

        for name, provider in six.iteritems(overriding.providers):
            try:
                getattr(self, name).override(provider)
            except AttributeError:
                pass

    def reset_last_overriding(self):
        """Reset last overriding provider for each container providers.

        :rtype: None
        """
        if not self.overridden:
            raise Error('Container {0} is not overridden'.format(self))

        self.overridden = self.overridden[:-1]

        for provider in six.itervalues(self.providers):
            provider.reset_last_overriding()

    def reset_override(self):
        """Reset all overridings for each container providers.

        :rtype: None
        """
        self.overridden = tuple()

        for provider in six.itervalues(self.providers):
            provider.reset_override()
