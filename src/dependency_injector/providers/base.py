"""Dependency injector base providers."""

import six

from dependency_injector.errors import Error
from dependency_injector.utils import (
    is_provider,
    ensure_is_provider,
    represent_provider,
)


@six.python_2_unicode_compatible
class Provider(object):
    """Base provider class.

    :py:class:`Provider` is callable (implements ``__call__`` method). Every
    call to provider object returns provided result, according to the providing
    strategy of particular provider. This ``callable`` functionality is a
    regular part of providers API and it should be the same for all provider's
    subclasses.

    Implementation of particular providing strategy should be done in
    :py:meth:`Provider._provide` of :py:class:`Provider` subclass. Current
    method is called every time when not overridden provider is called.

    :py:class:`Provider` implements provider overriding logic that should be
    also common for all providers:

    .. code-block:: python

        provider1 = Factory(SomeClass)
        provider2 = Factory(ChildSomeClass)

        provider1.override(provider2)

        some_instance = provider1()
        assert isinstance(some_instance, ChildSomeClass)

    Also :py:class:`Provider` implements helper function for creating its
    delegates:

    .. code-block:: python

        provider = Factory(object)
        delegate = provider.delegate()

        delegated = delegate()

        assert provider is delegated

    All providers should extend this class.

    .. py:attribute:: overridden

        Tuple of overriding providers, if any.

        :type: tuple[:py:class:`Provider`] | None
    """

    __IS_PROVIDER__ = True
    __OPTIMIZED_CALLS__ = True
    __slots__ = ('overridden', 'provide', '__call__')

    def __init__(self):
        """Initializer."""
        self.overridden = tuple()
        super(Provider, self).__init__()
        # Enable __call__() / _provide() optimization
        if self.__class__.__OPTIMIZED_CALLS__:
            self.__call__ = self.provide = self._provide

    def _provide(self, *args, **kwargs):
        """Providing strategy implementation.

        Abstract protected method that implements providing strategy of
        particular provider. Current method is called every time when not
        overridden provider is called. Need to be overridden in subclasses.
        """
        raise NotImplementedError()

    def _call_last_overriding(self, *args, **kwargs):
        """Call last overriding provider and return result."""
        return (self.overridden[-1](*args, **kwargs)
                if self.overridden
                else None)

    def provide_injection(self):
        """Injection strategy implementation.

        :rtype: object
        """
        return self.provide()

    def override(self, provider):
        """Override provider with another provider.

        :param provider: Overriding provider.
        :type provider: :py:class:`Provider`

        :raise: :py:exc:`dependency_injector.errors.Error`

        :return: Overriding provider.
        :rtype: :py:class:`Provider`
        """
        if provider is self:
            raise Error('Provider {0} could not be overridden '
                        'with itself'.format(self))

        if not is_provider(provider):
            provider = Object(provider)

        self.overridden += (ensure_is_provider(provider),)

        # Disable __call__() / _provide() optimization
        if self.__class__.__OPTIMIZED_CALLS__:
            self.__call__ = self.provide = self._call_last_overriding

        return OverridingContext(self, provider)

    def reset_last_overriding(self):
        """Reset last overriding provider.

        :raise: :py:exc:`dependency_injector.errors.Error` if provider is not
                overridden.

        :rtype: None
        """
        if not self.overridden:
            raise Error('Provider {0} is not overridden'.format(str(self)))

        self.overridden = self.overridden[:-1]

        if not self.overridden:
            # Enable __call__() / _provide() optimization
            if self.__class__.__OPTIMIZED_CALLS__:
                self.__call__ = self.provide = self._provide

    def reset_override(self):
        """Reset all overriding providers.

        :rtype: None
        """
        self.overridden = tuple()

        # Enable __call__() / _provide() optimization
        if self.__class__.__OPTIMIZED_CALLS__:
            self.__call__ = self.provide = self._provide

    def delegate(self):
        """Return provider's delegate.

        :rtype: :py:class:`Delegate`
        """
        return Delegate(self)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=None)

    __repr__ = __str__


@six.python_2_unicode_compatible
class Delegate(Provider):
    """:py:class:`Delegate` provider delegates another provider.

    .. code-block:: python

        provider = Factory(object)
        delegate = Delegate(provider)

        delegated = delegate()

        assert provider is delegated

    .. py:attribute:: delegated

        Delegated provider.

        :type: :py:class:`Provider`
    """

    __slots__ = ('delegated',)

    def __init__(self, delegated):
        """Initializer.

        :provider delegated: Delegated provider.
        :type delegated: :py:class:`Provider`
        """
        self.delegated = ensure_is_provider(delegated)
        super(Delegate, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        return self.delegated

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.delegated)

    __repr__ = __str__


@six.python_2_unicode_compatible
class Object(Provider):
    """:py:class:`Object` provider returns provided instance "as is".

    .. py:attribute:: provides

        Value that have to be provided.

        :type: object
    """

    __slots__ = ('provides',)

    def __init__(self, provides):
        """Initializer.

        :param provides: Value that have to be provided.
        :type provides: object
        """
        self.provides = provides
        super(Object, self).__init__()

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        return self.provides

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.provides)

    __repr__ = __str__


@six.python_2_unicode_compatible
class ExternalDependency(Provider):
    """:py:class:`ExternalDependency` provider describes dependency interface.

    This provider is used for description of dependency interface. That might
    be useful when dependency could be provided in the client's code only,
    but it's interface is known. Such situations could happen when required
    dependency has non-determenistic list of dependencies itself.

    .. code-block:: python

        database_provider = ExternalDependency(sqlite3.dbapi2.Connection)
        database_provider.override(Factory(sqlite3.connect, ':memory:'))

        database = database_provider()

    .. py:attribute:: instance_of

        Class of required dependency.

        :type: type
    """

    __OPTIMIZED_CALLS__ = False
    __slots__ = ('instance_of',)

    def __init__(self, instance_of):
        """Initializer."""
        if not isinstance(instance_of, six.class_types):
            raise Error('ExternalDependency provider expects to get class, ' +
                        'got {0} instead'.format(str(instance_of)))
        self.instance_of = instance_of
        self.provide = self.__call__
        super(ExternalDependency, self).__init__()

    def __call__(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :raise: :py:exc:`dependency_injector.errors.Error`

        :rtype: object
        """
        if not self.overridden:
            raise Error('Dependency is not defined')

        instance = self._call_last_overriding(*args, **kwargs)

        if not isinstance(instance, self.instance_of):
            raise Error('{0} is not an '.format(instance) +
                        'instance of {0}'.format(self.instance_of))

        return instance

    def provided_by(self, provider):
        """Set external dependency provider.

        :param provider: Provider that provides required dependency.
        :type provider: :py:class:`Provider`

        :rtype: None
        """
        return self.override(provider)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.instance_of)

    __repr__ = __str__


class OverridingContext(object):
    """Provider overriding context.

    :py:class:`OverridingContext` is used by :py:meth:`Provider.override` for
    implemeting ``with`` contexts. When :py:class:`OverridingContext` is
    closed, overriding that was created in this context is dropped also.

    .. code-block:: python

        with provider.override(another_provider):
            assert provider.overridden
        assert not provider.overridden
    """

    def __init__(self, overridden, overriding):
        """Initializer.

        :param overridden: Overridden provider.
        :type overridden: :py:class:`Provider`

        :param overriding: Overriding provider.
        :type overriding: :py:class:`Provider`
        """
        self.overridden = overridden
        self.overriding = overriding

    def __enter__(self):
        """Do nothing."""
        return self.overriding

    def __exit__(self, *_):
        """Exit overriding context."""
        self.overridden.reset_last_overriding()


def override(overridden):
    """Decorator for overriding providers.

    This decorator overrides ``overridden`` provider by decorated one.

    .. code-block:: python

        @Factory
        class SomeClass(object):
            pass


        @override(SomeClass)
        @Factory
        class ExtendedSomeClass(SomeClass.cls):
            pass

    :param overridden: Provider that should be overridden.
    :type overridden: :py:class:`Provider`

    :return: Overriding provider.
    :rtype: :py:class:`Provider`
    """
    def decorator(overriding):
        overridden.override(overriding)
        return overriding
    return decorator


def _parse_positional_injections(args):
    return tuple(arg if is_provider(arg) else Object(arg)
                 for arg in args)


def _parse_keyword_injections(kwargs):
    return dict((name, arg if is_provider(arg) else Object(arg))
                for name, arg in six.iteritems(kwargs))
