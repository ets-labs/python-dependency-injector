"""
Standard providers.
"""

from collections import Iterable
from .injections import Injection, InitArg, Attribute, Method


class Provider(object):
    """
    Base provider class.
    """

    __is_objects_provider__ = True
    __overridden_by__ = list()

    def __init__(self):
        """
        Initializer.
        """
        self.__overridden_by__ = list()

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        raise NotImplementedError()

    def __override__(self, provider):
        """
        Overrides provider with another provider.
        """
        self.__overridden_by__.append(provider)


def prepare_injections(injections):
    """
    Prepares injections list to injection.
    """
    return [(injection.name, injection.value) for injection in injections]


def fetch_injections(injections, injection_type):
    """
    Fetches injections of injection type from list.
    """
    return tuple([injection
                  for injection in injections
                  if isinstance(injection, injection_type)])


class NewInstance(Provider):
    """
    New instance providers will create and return new instance on every call.
    """

    def __init__(self, provides, *injections):
        """
        Initializer.
        """
        self.provides = provides
        self.init_injections = fetch_injections(injections, InitArg)
        self.attribute_injections = fetch_injections(injections, Attribute)
        self.method_injections = fetch_injections(injections, Method)
        super(NewInstance, self).__init__()

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        if self.__overridden_by__:
            return self.__overridden_by__[-1].__call__(*args, **kwargs)

        init_injections = prepare_injections(self.init_injections)
        init_injections = dict(init_injections)
        init_injections.update(kwargs)

        provided = self.provides(*args, **init_injections)

        attribute_injections = prepare_injections(self.attribute_injections)
        for name, injectable in attribute_injections:
            setattr(provided, name, injectable)

        method_injections = prepare_injections(self.method_injections)
        for name, injectable in method_injections:
            getattr(provided, name)(injectable)

        return provided


class Singleton(NewInstance):
    """
    Singleton provider will create instance once and return it on every call.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializer.
        """
        self.instance = None
        super(Singleton, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        if not self.instance:
            self.instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.instance

    def _reset_instance(self):
        """
        Resets instance.
        """
        self.instance = None


class Scoped(Singleton):
    """
    Scoped provider will create instance once for every scope and return it on every call.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializer.
        """
        self.is_in_scope = None
        super(Scoped, self).__init__(*args, **kwargs)

    def in_scope(self):
        """
        Sets provider in "in scope" state.
        """
        self.is_in_scope = True
        self._reset_instance()

    def out_of_scope(self):
        """
        Sets provider in "out of scope" state.
        """
        self.is_in_scope = False
        self._reset_instance()

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        if not self.is_in_scope:
            raise RuntimeError('Trying to provide {} while provider is not in scope'.format(self.provides))
        return super(Scoped, self).__call__(*args, **kwargs)

    def __enter__(self):
        """
        With __enter__() implementation. Makes provider to be in scope.
        """
        self.in_scope()
        return self

    def __exit__(self, *_):
        """
        With __exit__() implementation. Makes provider to be out of scope.
        """
        self.out_of_scope()


class ExternalDependency(Provider):
    """
    External dependency provider.
    """

    def __init__(self, instance_of):
        """
        Initializer

        :param instance_of: type
        """
        if not isinstance(instance_of, Iterable):
            instance_of = (instance_of,)
        self.instance_of = instance_of
        self.dependency = None
        super(ExternalDependency, self).__init__()

    def satisfy(self, provider):
        """
        Satisfies an external dependency.

        :param provider: Provider
        """
        self.dependency = provider

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        if not self.dependency:
            raise ValueError('Dependency is not satisfied')

        result = self.dependency.__call__(*args, **kwargs)

        if not any((isinstance(result, possible_type) for possible_type in self.instance_of)):
            raise TypeError('{} is not an instance of {}'.format(result, self.instance_of))

        return result


class _StaticProvider(Provider):
    """
    Static provider is base implementation that provides exactly the same as
    it got on input.
    """

    def __init__(self, provides):
        """
        Initializer.
        """
        self.provides = provides
        super(_StaticProvider, self).__init__()

    def __call__(self):
        """
        Returns provided instance.
        """
        if self.__overridden_by__:
            return self.__overridden_by__[-1].__call__()
        return self.provides


class Class(_StaticProvider):
    """
    Class provider provides class.
    """


class Object(_StaticProvider):
    """
    Object provider provides object.
    """


class Function(_StaticProvider):
    """
    Function provider provides function.
    """


class Value(_StaticProvider):
    """
    Value provider provides value.
    """


class Callable(Provider):
    """
    Callable provider will provide callable calls with some predefined
    dependencies injections.
    """

    def __init__(self, calls, *injections):
        """
        Initializer.
        """
        self.calls = calls
        self.injections = fetch_injections(injections, Injection)
        super(Callable, self).__init__()

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        if self.__overridden_by__:
            return self.__overridden_by__[-1].__call__(*args, **kwargs)

        injections = prepare_injections(self.injections)
        injections = dict(injections)
        injections.update(kwargs)

        return self.calls(*args, **injections)


class _DeferredConfig(Provider):
    """
    Deferred config providers provide an value from the root config object.
    """
    def __init__(self, paths, root_config):
        """
        Initializer.
        """
        self.paths = paths
        self.root_config = root_config
        super(_DeferredConfig, self).__init__()

    def __getattr__(self, item):
        """
        Returns instance of deferred config.
        """
        return _DeferredConfig(paths=self.paths + (item,),
                               root_config=self.root_config)

    def __call__(self, *args, **kwargs):
        """
        Returns provided instance.
        """
        return self.root_config(self.paths)


class Config(Provider):
    """
    Config provider provides dict values. Also config provider creates
    deferred config objects for all undefined attribute calls.
    """

    def __init__(self, value=None):
        """
        Initializer.
        """
        if not value:
            value = dict()
        self.value = value
        super(Config, self).__init__()

    def update_from(self, value):
        """
        Updates current value from another one.
        """
        self.value.update(value)

    def __getattr__(self, item):
        """
        Returns instance of deferred config.
        """
        return _DeferredConfig(paths=(item,),
                               root_config=self)

    def __call__(self, paths=None):
        """
        Returns provided instance.
        """
        value = self.value
        if paths:
            for path in paths:
                value = value[path]
        return value
