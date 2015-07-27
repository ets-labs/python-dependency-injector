"""Providers module."""

from six import class_types

from .utils import ensure_is_provider
from .utils import is_kwarg_injection
from .utils import is_attribute_injection
from .utils import is_method_injection
from .utils import get_injectable_kwargs

from .errors import Error


class Provider(object):

    """Base provider class."""

    __IS_PROVIDER__ = True
    __slots__ = ('_overridden',)

    def __init__(self):
        """Initializer."""
        self._overridden = None

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if self._overridden:
            return self.last_overriding(*args, **kwargs)
        return self._provide(*args, **kwargs)

    def _provide(self, *args, **kwargs):
        """Providing strategy implementation.

        Abstract protected method that implements providing strategy of
        particular provider. Current method is called every time when not
        overridden provider is called. Need to be overridden in subclasses.
        """
        raise NotImplementedError()

    def delegate(self):
        """Return provider's delegate."""
        return Delegate(self)

    def override(self, provider):
        """Override provider with another provider."""
        if not self._overridden:
            self._overridden = (ensure_is_provider(provider),)
        else:
            self._overridden += (ensure_is_provider(provider),)

    @property
    def is_overridden(self):
        """Check if provider is overridden by another provider."""
        return bool(self._overridden)

    @property
    def last_overriding(self):
        """Return last overriding provider."""
        try:
            return self._overridden[-1]
        except (TypeError, IndexError):
            raise Error('Provider {0} is not overridden'.format(str(self)))

    def reset_last_overriding(self):
        """Reset last overriding provider."""
        if not self._overridden:
            raise Error('Provider {0} is not overridden'.format(str(self)))
        self._overridden = self._overridden[:-1]

    def reset_override(self):
        """Reset all overriding providers."""
        self._overridden = None


class Delegate(Provider):

    """Provider's delegate."""

    __slots__ = ('_delegated',)

    def __init__(self, delegated):
        """Initializer.

        :type delegated: Provider
        """
        self._delegated = ensure_is_provider(delegated)
        super(Delegate, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance."""
        return self._delegated


class Factory(Provider):

    """Factory provider.

    Factory provider creates new instance of specified class on every call.
    """

    __slots__ = ('_provides', '_kwargs', '_attributes', '_methods')

    def __init__(self, provides, *injections):
        """Initializer."""
        if not callable(provides):
            raise Error('Factory provider expects to get callable, ' +
                        'got {0} instead'.format(str(provides)))
        self._provides = provides
        self._kwargs = tuple((injection
                              for injection in injections
                              if is_kwarg_injection(injection)))
        self._attributes = tuple((injection
                                  for injection in injections
                                  if is_attribute_injection(injection)))
        self._methods = tuple((injection
                               for injection in injections
                               if is_method_injection(injection)))
        super(Factory, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance."""
        instance = self._provides(*args,
                                  **get_injectable_kwargs(kwargs,
                                                          self._kwargs))
        for attribute in self._attributes:
            setattr(instance, attribute.name, attribute.value)
        for method in self._methods:
            getattr(instance, method.name)(method.value)

        return instance


class NewInstance(Factory):

    """NewInstance provider.

    It is synonym of Factory provider. NewInstance provider is considered to
    be deprecated, but will be able to use for further backward
    compatibility.
    """


class Singleton(Provider):

    """Singleton provider.

    Singleton provider will create instance once and return it on every call.
    """

    __slots__ = ('_instance', '_factory')

    def __init__(self, provides, *injections):
        """Initializer."""
        self._instance = None
        self._factory = Factory(provides, *injections)
        super(Singleton, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance."""
        if not self._instance:
            self._instance = self._factory(*args, **kwargs)
        return self._instance

    def reset(self):
        """Reset instance."""
        self._instance = None


class ExternalDependency(Provider):

    """External dependency provider.

    Those provider is used when dependency obviously have to be overridden by
    the client's code, but it's interface is known.
    """

    __slots__ = ('_instance_of',)

    def __init__(self, instance_of):
        """Initializer."""
        if not isinstance(instance_of, class_types):
            raise Error('ExternalDependency provider expects to get class, ' +
                        'got {0} instead'.format(str(instance_of)))
        self._instance_of = instance_of
        super(ExternalDependency, self).__init__()

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if not self._overridden:
            raise Error('Dependency is not defined')

        instance = self.last_overriding(*args, **kwargs)

        if not isinstance(instance, self._instance_of):
            raise Error('{0} is not an '.format(instance) +
                        'instance of {0}'.format(self._instance_of))

        return instance

    def provided_by(self, provider):
        """Set external dependency provider."""
        return self.override(provider)


class _StaticProvider(Provider):

    """Static provider.

    Static provider is base implementation that provides exactly the same as
    it got on input.
    """

    __slots__ = ('_provides',)

    def __init__(self, provides):
        """Initializer."""
        self._provides = provides
        super(_StaticProvider, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance."""
        return self._provides


class Class(_StaticProvider):

    """Class provider provides class."""


class Object(_StaticProvider):

    """Object provider provides object."""


class Function(_StaticProvider):

    """Function provider provides function."""


class Value(_StaticProvider):

    """Value provider provides value."""


class Callable(Provider):

    """Callable provider.

    Callable provider provides callable that is called on every provider call
    with some predefined dependency injections.
    """

    __slots__ = ('_callback', '_injections')

    def __init__(self, callback, *injections):
        """Initializer."""
        if not callable(callback):
            raise Error('Callable expected, got {0}'.format(str(callback)))
        self._callback = callback
        self._injections = tuple((injection
                                  for injection in injections
                                  if is_kwarg_injection(injection)))
        super(Callable, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance."""
        return self._callback(*args, **get_injectable_kwargs(kwargs,
                                                             self._injections))


class Config(Provider):

    """Config provider.

    Config provider provides dict values. Also config provider creates
    child config objects for all undefined attribute calls. It makes possible
    to create deferred config value provider.
    """

    __slots__ = ('_value',)

    def __init__(self, value=None):
        """Initializer."""
        if not value:
            value = dict()
        self._value = value
        super(Config, self).__init__()

    def __getattr__(self, item):
        """Return instance of deferred config."""
        return _ChildConfig(parents=(item,), root_config=self)

    def _provide(self, paths=None):
        """Return provided instance."""
        value = self._value
        if paths:
            for path in paths:
                try:
                    value = value[path]
                except KeyError:
                    raise Error('Config key '
                                '"{0}" is undefined'.format('.'.join(paths)))
        return value

    def update_from(self, value):
        """Update current value from another one."""
        self._value.update(value)


class _ChildConfig(Provider):

    """Child config provider.

    Child config provide an value from the root config object according to
    the current path in the config tree.
    """

    __slots__ = ('_parents', '_root_config')

    def __init__(self, parents, root_config):
        """Initializer."""
        self._parents = parents
        self._root_config = root_config
        super(_ChildConfig, self).__init__()

    def __getattr__(self, item):
        """Return instance of deferred config."""
        return _ChildConfig(parents=self._parents + (item,),
                            root_config=self._root_config)

    def _provide(self, *args, **kwargs):
        """Return provided instance."""
        return self._root_config(self._parents)
