"""Providers module."""

from inspect import isclass
from collections import Iterable

from .utils import ensure_is_provider
from .utils import is_injection
from .utils import is_init_arg_injection
from .utils import is_attribute_injection
from .utils import is_method_injection

from .errors import Error


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
        return Delegate(self)

    def override(self, provider):
        """Override provider with another provider."""
        self.overridden.append(ensure_is_provider(provider))

    @property
    def last_overriding(self):
        """Return last overriding provider."""
        try:
            return self.overridden[-1]
        except IndexError:
            raise Error('Provider {} '.format(str(self)) +
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

    __slots__ = ('provides', 'init_args', 'attributes', 'methods')

    def __init__(self, provides, *injections):
        """Initializer."""
        if not isclass(provides):
            raise Error('NewInstance provider expects to get class, ' +
                        'got {} instead'.format(str(provides)))
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

        init_kwargs = dict(((injection.name, injection.value)
                            for injection in self.init_args))
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


class Scoped(NewInstance):

    """Scoped provider.

    Scoped provider will create instance once for every scope and return it
    on every call.
    """

    __slots__ = ('current_scope', 'scopes_to_instances')

    def __init__(self, *args, **kwargs):
        """Initializer."""
        self.current_scope = None
        self.scopes_to_instances = dict()
        super(Scoped, self).__init__(*args, **kwargs)

    def in_scope(self, scope):
        """Set provider in "in scope" state."""
        self.current_scope = scope

    def out_of_scope(self, scope):
        """Set provider in "out of scope" state."""
        self.current_scope = None
        try:
            del self.scopes_to_instances[scope]
        except KeyError:
            raise Error('Trying to move out of undefined scope '
                        '"{}"'.format(scope))

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if not self.current_scope:
            raise Error('Trying to provide {} '.format(self.provides) +
                        'while provider has no active scope')
        try:
            instance = self.scopes_to_instances[self.current_scope]
        except KeyError:
            instance = super(Scoped, self).__call__(*args, **kwargs)
            self.scopes_to_instances[self.current_scope] = instance
        return instance


class ExternalDependency(Provider):

    """External dependency provider."""

    __slots__ = ('instance_of', 'dependency')

    def __init__(self, instance_of):
        """Initializer."""
        self.instance_of = instance_of
        self.dependency = None
        super(ExternalDependency, self).__init__()

    def satisfy(self, provider):
        """Satisfy an external dependency."""
        self.dependency = ensure_is_provider(provider)

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        if not self.dependency:
            raise Error('Dependency is not satisfied')

        instance = self.dependency.__call__(*args, **kwargs)

        if not isinstance(instance, self.instance_of):
            raise Error('{} is not an '.format(instance) +
                        'instance of {}'.format(self.instance_of))

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
        return _DeferredConfig(parents=(item,),
                               root_config=self)

    def __call__(self, paths=None):
        """Return provided instance."""
        value = self.value
        if paths:
            for path in paths:
                value = value[path]
            return value


class _DeferredConfig(Provider):

    """Deferred config provider.

    Deferred config providers provide an value from the root config object.
    """

    __slots__ = ('parents', 'root_config')

    def __init__(self, parents, root_config):
        """Initializer."""
        self.parents = parents
        self.root_config = root_config
        super(_DeferredConfig, self).__init__()

    def __getattr__(self, item):
        """Return instance of deferred config."""
        return _DeferredConfig(parents=self.parents + (item,),
                               root_config=self.root_config)

    def __call__(self, *args, **kwargs):
        """Return provided instance."""
        return self.root_config(self.parents)
