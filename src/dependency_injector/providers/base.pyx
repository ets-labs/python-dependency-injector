"""Dependency injector base providers.

Powered by Cython.
"""

cimport cython

from dependency_injector.errors import Error

from .utils cimport (
    CLASS_TYPES,
    is_provider,
    ensure_is_provider,
    represent_provider,
    deepcopy,
)


cdef class Provider(object):
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

    def __init__(self):
        """Initializer."""
        self.__overridden = tuple()
        self.__overridden_len = 0
        super(Provider, self).__init__()

    def __call__(self, *args, **kwargs):
        """Return provided object.

        Callable interface implementation.
        """
        if self.__overridden_len != 0:
            return self._call_last_overriding(args, kwargs)
        return self._provide(args, kwargs)

    def __deepcopy__(self, memo):
        """Create and return full copy of provider."""
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__()

        for overriding_provider in self.overridden:
            copied.override(deepcopy(overriding_provider, memo))

        return copied

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=None)

    def __repr__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return self.__str__()

    @property
    def overridden(self):
        """Return tuple of overriding providers."""
        return self.__overridden

    def override(self, provider):
        """Override provider with another provider.

        :param provider: Overriding provider.
        :type provider: :py:class:`Provider`

        :raise: :py:exc:`dependency_injector.errors.Error`

        :return: Overriding context.
        :rtype: :py:class:`OverridingContext`
        """
        if provider is self:
            raise Error('Provider {0} could not be overridden '
                        'with itself'.format(self))

        if not is_provider(provider):
            provider = Object(provider)

        self.__overridden += (provider,)
        self.__overridden_len += 1

        return OverridingContext(self, provider)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def reset_last_overriding(self):
        """Reset last overriding provider.

        :raise: :py:exc:`dependency_injector.errors.Error` if provider is not
                overridden.

        :rtype: None
        """
        if self.__overridden_len == 0:
            raise Error('Provider {0} is not overridden'.format(str(self)))

        self.__overridden = self.__overridden[:self.__overridden_len - 1]
        self.__overridden_len -= 1

    def reset_override(self):
        """Reset all overriding providers.

        :rtype: None
        """
        self.__overridden = tuple()
        self.__overridden_len = 0

    def delegate(self):
        """Return provider's delegate.

        :rtype: :py:class:`Delegate`
        """
        return Delegate(self)

    cpdef object _provide(self, tuple args, dict kwargs):
        """Providing strategy implementation.

        Abstract protected method that implements providing strategy of
        particular provider. Current method is called every time when not
        overridden provider is called. Need to be overridden in subclasses.
        """
        raise NotImplementedError()

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef object _call_last_overriding(self, tuple args, dict kwargs):
        """Call last overriding provider and return result."""
        return  <object>self.__overridden[self.__overridden_len - 1](*args,
                                                                     **kwargs)


cdef class Object(Provider):
    """Object provider returns provided instance "as is".

    .. py:attribute:: provides

        Value that have to be provided.

        :type: object
    """

    def __init__(self, provides):
        """Initializer.

        :param provides: Value that have to be provided.
        :type provides: object
        """
        self.__provides = provides
        super(Object, self).__init__()

    def __deepcopy__(self, memo):
        """Create and return full copy of provider."""
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__(deepcopy(self.__provides, memo))

        for overriding_provider in self.overridden:
            copied.override(deepcopy(overriding_provider, memo))

        return copied

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.__provides)

    def __repr__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return self.__str__()

    cpdef object _provide(self, tuple args, dict kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        return self.__provides


cdef class Delegate(Object):
    """Delegate provider returns provider "as is".

    .. py:attribute:: provides

        Value that have to be provided.

        :type: object
    """

    def __init__(self, provides):
        """Initializer.

        :param provides: Value that have to be provided.
        :type provides: object
        """
        super(Delegate, self).__init__(ensure_is_provider(provides))


cdef class ExternalDependency(Provider):
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

    def __init__(self, type instance_of):
        """Initializer."""
        self.__instance_of = instance_of
        super(ExternalDependency, self).__init__()

    def __deepcopy__(self, memo):
        """Create and return full copy of provider."""
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__(self.__instance_of)

        for overriding_provider in self.overridden:
            copied.override(deepcopy(overriding_provider, memo))

        return copied

    def __call__(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :raise: :py:exc:`dependency_injector.errors.Error`

        :rtype: object
        """
        cdef object instance

        if self.__overridden_len == 0:
            raise Error('Dependency is not defined')

        instance = self._call_last_overriding(args, kwargs)

        if not isinstance(instance, self.instance_of):
            raise Error('{0} is not an '.format(instance) +
                        'instance of {0}'.format(self.instance_of))

        return instance

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.__instance_of)

    def __repr__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return self.__str__()

    @property
    def instance_of(self):
        """Return class of required dependency."""
        return self.__instance_of

    def provided_by(self, provider):
        """Set external dependency provider.

        :param provider: Provider that provides required dependency.
        :type provider: :py:class:`Provider`

        :rtype: None
        """
        return self.override(provider)


cdef class OverridingContext(object):
    """Provider overriding context.

    :py:class:`OverridingContext` is used by :py:meth:`Provider.override` for
    implemeting ``with`` contexts. When :py:class:`OverridingContext` is
    closed, overriding that was created in this context is dropped also.

    .. code-block:: python

        with provider.override(another_provider):
            assert provider.overridden
        assert not provider.overridden
    """

    def __init__(self, Provider overridden, Provider overriding):
        """Initializer.

        :param overridden: Overridden provider.
        :type overridden: :py:class:`Provider`

        :param overriding: Overriding provider.
        :type overriding: :py:class:`Provider`
        """
        self.__overridden = overridden
        self.__overriding = overriding
        super(OverridingContext, self).__init__()

    def __enter__(self):
        """Do nothing."""
        return self.__overriding

    def __exit__(self, *_):
        """Exit overriding context."""
        self.__overridden.reset_last_overriding()
