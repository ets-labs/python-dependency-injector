"""Providers module."""

from collections import Iterable

from .utils import is_provider
from .utils import is_injection
from .utils import is_init_arg_injection
from .utils import is_attribute_injection
from .utils import is_method_injection


class Provider(object):

    """Base provider class."""

    __IS_OBJECTS_PROVIDER__ = True
    __slots__ = ('__IS_OBJECTS_PROVIDER__', 'overridden')

    def __init__(self):
        """Initializer."""
        self.overridden = list()

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        raise NotImplementedError()

    def delegate(self):
        """Return provider's delegate."""
        return ProviderDelegate(self)

    def override(self, provider):
        """Override provider with another provider."""
        if not is_provider(provider):
            raise TypeError('Expected provider as an overriding instance, '
                            'got {}'.format(str(provider)))
        self.overridden.append(provider)

    @property
    def last_overriding(self):
        """Return last overriding provider."""
        try:
            return self.overridden[-1]
        except IndexError:
            raise AttributeError('Provider {} '.format(str(self)) +
                                 'is not overridden')


class ProviderDelegate(Provider):

    """Provider's delegate."""

    __slots__ = ('delegated',)

    def __init__(self, delegated):
        """Initializer.

        :type delegated: Provider
        """
        self.delegated = delegated
        super(ProviderDelegate, self).__init__()

    def __call__(self):
        """Return provided instance."""
        return self.delegated


class NewInstance(Provider):

    """New instance provider.

    New instance providers will create and return new instance on every call.
    """

    __slots__ = ('provides', 'init_args', 'attributes', 'methods')

    def __init__(self, provides, *injections):
        """Initializer."""
        self.provides = provides
        self.init_args = tuple((injection
                                for injection in injections
                                if is_init_arg_injection(injection)))
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

        init_injections = dict(((injection.name, injection.value)
                                for injection in self.init_args))
        init_injections.update(kwargs)

        instance = self.provides(*args, **init_injections)

        if not self.attributes:
            for injection in self.attributes:
                setattr(instance, injection.name, injection.value)

        if not self.methods:
            for injection in self.methods:
                getattr(instance, injection.name)(injection.value)

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

    def _reset_instance(self):
        """Reset instance."""
        self.instance = None


class Scoped(Singleton):

    """Scoped provider.

    Scoped provider will create instance once for every scope and return it
    on every call.
    """

    __slots__ = ('is_in_scope',)

    def __init__(self, *args, **kwargs):
        """Initializer."""
        self.is_in_scope = None
        super(Scoped, self).__init__(*args, **kwargs)

    def in_scope(self):
        """Set provider in "in scope" state."""
        self.is_in_scope = True
        self._reset_instance()

    def out_of_scope(self):
        """Set provider in "out of scope" state."""
        self.is_in_scope = False
        self._reset_instance()

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if not self.is_in_scope:
            raise RuntimeError('Trying to provide {} '.format(self.provides) +
                               'while provider is not in scope')
        return super(Scoped, self).__call__(*args, **kwargs)

    def __enter__(self):
        """Make provider to be in scope."""
        self.in_scope()
        return self

    def __exit__(self, *_):
        """Make provider to be out of scope."""
        self.out_of_scope()


class ExternalDependency(Provider):

    """External dependency provider."""

    __slots__ = ('instance_of', 'dependency')

    def __init__(self, instance_of):
        """Initializer."""
        if not isinstance(instance_of, Iterable):
            instance_of = (instance_of,)
        self.instance_of = instance_of
        self.dependency = None
        super(ExternalDependency, self).__init__()

    def satisfy(self, provider):
        """Satisfy an external dependency."""
        self.dependency = provider

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if not self.dependency:
            raise ValueError('Dependency is not satisfied')

        result = self.dependency.__call__(*args, **kwargs)

        is_instance = any((isinstance(result, possible_type)
                           for possible_type in self.instance_of))

        if not is_instance:
            raise TypeError('{} is not an '.format(result) +
                            'instance of {}'.format(self.instance_of))

        return result


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

    Callable provider will provide callable calls with some predefined
    dependencies injections.
    """

    __slots__ = ('calls', 'injections')

    def __init__(self, calls, *injections):
        """Initializer."""
        self.calls = calls
        self.injections = tuple((injection
                                 for injection in injections
                                 if is_injection(injection)))
        super(Callable, self).__init__()

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if self.overridden:
            return self.last_overriding()

        injections = dict(((injection.name, injection.value)
                           for injection in self.injections))
        injections.update(kwargs)

        return self.calls(*args, **injections)


class Config(Provider):

    """Config provider.

    Config provider provides dict values. Also config provider creates
    deferred config objects for all undefined attribute calls.
    """

    __slots__ = ('value',)

    def __init__(self, value=None):
        """Initializer."""
        if not value:
            value = dict()
        self.value = value
        super(Config, self).__init__()

    def update_from(self, value):
        """Update current value from another one."""
        self.value.update(value)

    def __getattr__(self, item):
        """Return instance of deferred config."""
        return _DeferredConfig(paths=(item,),
                               root_config=self)

    def __call__(self, paths=None):
        """Return provided instance."""
        value = self.value
        if paths:
            for path in paths:
                value = value[path]
            return valueg


class _DeferredConfig(Provider):

    """Deferred config provider.

    Deferred config providers provide an value from the root config object.
    """

    __slots__ = ('paths', 'root_config')

    def __init__(self, paths, root_config):
        """Initializer."""
        self.paths = paths
        self.root_config = root_config
        super(_DeferredConfig, self).__init__()

    def __getattr__(self, item):
        """Return instance of deferred config."""
        return _DeferredConfig(paths=self.paths + (item,),
                               root_config=self.root_config)

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        return self.root_config(self.paths)
