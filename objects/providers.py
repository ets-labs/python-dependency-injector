"""Providers module."""

from six import class_types

from .utils import ensure_is_provider
from .utils import is_kwarg_injection
from .utils import is_attribute_injection
from .utils import is_method_injection

from .errors import Error


class Provider(object):

    """Base provider class."""

    __IS_OBJECTS_PROVIDER__ = True
    __slots__ = ('__IS_OBJECTS_PROVIDER__', 'overridden')

    def __init__(self):
        """Initializer."""
        self.overridden = None

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        raise NotImplementedError()

    def delegate(self):
        """Return provider's delegate."""
        return Delegate(self)

    def override(self, provider):
        """Override provider with another provider."""
        if not self.overridden:
            self.overridden = (ensure_is_provider(provider),)
        else:
            self.overridden = self.overridden + (ensure_is_provider(provider),)

    def reset_override(self):
        """Reset all overriding providers."""
        self.overridden = None

    @property
    def last_overriding(self):
        """Return last overriding provider."""
        try:
            return self.overridden[-1]
        except (TypeError, IndexError):
            raise Error('Provider {0} '.format(str(self)) +
                        'is not overridden')


class Delegate(Provider):

    """Provider's delegate."""

    __slots__ = ('delegated',)

    def __init__(self, delegated):
        """Initializer.

        :type delegated: Provider
        """
        self.delegated = ensure_is_provider(delegated)
        super(Delegate, self).__init__()

    def __call__(self):
        """Return provided instance."""
        return self.delegated


class NewInstance(Provider):

    """New instance provider.

    New instance providers will create and return new instance on every call.
    """

    __slots__ = ('provides', 'kwargs', 'attributes', 'methods')

    def __init__(self, provides, *injections):
        """Initializer."""
        if not isinstance(provides, class_types):
            raise Error('NewInstance provider expects to get class, ' +
                        'got {0} instead'.format(str(provides)))
        self.provides = provides
        self.kwargs = tuple((injection
                             for injection in injections
                             if is_kwarg_injection(injection)))
        self.attributes = tuple((injection
                                 for injection in injections
                                 if is_attribute_injection(injection)))
        self.methods = tuple((injection
                              for injection in injections
                              if is_method_injection(injection)))
        super(NewInstance, self).__init__()

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if self.overridden:
            return self.last_overriding(*args, **kwargs)

        init_kwargs = dict(((injection.name, injection.value)
                            for injection in self.kwargs))
        init_kwargs.update(kwargs)

        instance = self.provides(*args, **init_kwargs)

        for attribute in self.attributes:
            setattr(instance, attribute.name, attribute.value)
        for method in self.methods:
            getattr(instance, method.name)(method.value)

        return instance


class Singleton(NewInstance):

    """Singleton provider.

    Singleton provider will create instance once and return it on every call.
    """

    __slots__ = ('instance',)

    def __init__(self, *args, **kwargs):
        """Initializer."""
        self.instance = None
        super(Singleton, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if not self.instance:
            self.instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.instance

    def reset(self):
        """Reset instance."""
        self.instance = None


class ExternalDependency(Provider):

    """External dependency provider.

    Those provider is used when dependency obviously have to be overridden by
    the client's code, but it's interface is known.
    """

    __slots__ = ('instance_of',)

    def __init__(self, instance_of):
        """Initializer."""
        if not isinstance(instance_of, class_types):
            raise Error('ExternalDependency provider expects to get class, ' +
                        'got {0} instead'.format(str(instance_of)))
        self.instance_of = instance_of
        super(ExternalDependency, self).__init__()

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if not self.overridden:
            raise Error('Dependency is not defined')

        instance = self.last_overriding(*args, **kwargs)

        if not isinstance(instance, self.instance_of):
            raise Error('{0} is not an '.format(instance) +
                        'instance of {0}'.format(self.instance_of))

        return instance


class _StaticProvider(Provider):

    """Static provider.

    Static provider is base implementation that provides exactly the same as
    it got on input.
    """

    __slots__ = ('provides',)

    def __init__(self, provides):
        """Initializer."""
        self.provides = provides
        super(_StaticProvider, self).__init__()

    def __call__(self):
        """Return provided instance."""
        if self.overridden:
            return self.last_overriding()
        return self.provides


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

    __slots__ = ('callback', 'injections')

    def __init__(self, callback, *injections):
        """Initializer."""
        if not callable(callback):
            raise Error('Callable expected, got {0}'.format(str(callback)))
        self.callback = callback
        self.injections = tuple((injection
                                 for injection in injections
                                 if is_kwarg_injection(injection)))
        super(Callable, self).__init__()

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if self.overridden:
            return self.last_overriding()

        injections = dict(((injection.name, injection.value)
                           for injection in self.injections))
        injections.update(kwargs)

        return self.callback(*args, **injections)


class Config(Provider):

    """Config provider.

    Config provider provides dict values. Also config provider creates
    child config objects for all undefined attribute calls. It makes possible
    to create deferred config value provider.
    """

    __slots__ = ('value',)

    def __init__(self, value=None):
        """Initializer."""
        if not value:
            value = dict()
        self.value = value
        super(Config, self).__init__()

    def __call__(self, paths=None):
        """Return provided instance."""
        value = self.value
        if paths:
            for path in paths:
                try:
                    value = value[path]
                except KeyError:
                    raise Error('Config key '
                                '"{0}" is undefined'.format('.'.join(paths)))
        return value

    def __getattr__(self, item):
        """Return instance of deferred config."""
        return _ChildConfig(parents=(item,), root_config=self)

    def update_from(self, value):
        """Update current value from another one."""
        self.value.update(value)


class _ChildConfig(Provider):

    """Child config provider.

    Child config provide an value from the root config object according to
    the current path in the config tree.
    """

    __slots__ = ('parents', 'root_config')

    def __init__(self, parents, root_config):
        """Initializer."""
        self.parents = parents
        self.root_config = root_config
        super(_ChildConfig, self).__init__()

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        return self.root_config(self.parents)

    def __getattr__(self, item):
        """Return instance of deferred config."""
        return _ChildConfig(parents=self.parents + (item,),
                            root_config=self.root_config)
