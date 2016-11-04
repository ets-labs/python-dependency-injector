"""Dependency injector base providers.

Powered by Cython.
"""

cimport cython

from dependency_injector.errors import Error

from .static cimport (
    Object,
    Delegate,
)
from .utils cimport (
    is_provider,
    ensure_is_provider,
    represent_provider,
    OverridingContext,
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

        print(self.__overridden, provider)
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
        if self.__overridden_len == 0:
            return None
        return  <object>self.__overridden[self.__overridden_len - 1](*args,
                                                                     **kwargs)
