"""Dependency injector singleton providers.

Powered by Cython.
"""

import threading

from dependency_injector.errors import Error

from .base cimport Provider
from .factories cimport (
    Factory,
    __factory_call,
)
from .utils cimport (
    represent_provider,
    deepcopy,
)


GLOBAL_LOCK = threading.RLock()
"""Global reentrant lock.

:type: :py:class:`threading.RLock`
"""


cdef class BaseSingleton(Provider):
    """Base class of singleton providers."""

    provided_type = None

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Provided type.
        :type provides: type

        :param args: Tuple of positional argument injections.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword argument injections.
        :type kwargs: dict[str, object]
        """
        if (self.__class__.provided_type and
                not issubclass(provides, self.__class__.provided_type)):
            raise Error('{0} can provide only {1} instances'.format(
                self.__class__, self.__class__.provided_type))

        self.__instantiator = Factory(provides, *args, **kwargs)

        super(BaseSingleton, self).__init__()

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self,
                                  provides=self.__instantiator.cls)

    def __deepcopy__(self, memo):
        """Create and return full copy of provider."""
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__(self.cls,
                                *deepcopy(self.args, memo),
                                **deepcopy(self.kwargs, memo))
        copied.set_attributes(**deepcopy(self.attributes, memo))

        for overriding_provider in self.overridden:
            copied.override(deepcopy(overriding_provider, memo))

        return copied

    @property
    def cls(self):
        """Return provided type."""
        return self.__instantiator.cls

    @property
    def args(self):
        """Return positional argument injections."""
        return self.__instantiator.args

    def add_args(self, *args):
        """Add __init__ postional argument injections.

        :param args: Tuple of injections.
        :type args: tuple

        :return: Reference ``self``
        """
        self.__instantiator.add_args(*args)
        return self

    def set_args(self, *args):
        """Set __init__ postional argument injections.

        Existing __init__ positional argument injections are dropped.

        :param args: Tuple of injections.
        :type args: tuple

        :return: Reference ``self``
        """
        self.__instantiator.set_args(*args)
        return self

    def clear_args(self):
        """Drop __init__ postional argument injections.

        :return: Reference ``self``
        """
        self.__instantiator.clear_args()
        return self

    @property
    def kwargs(self):
        """Return keyword argument injections."""
        return self.__instantiator.kwargs

    def add_kwargs(self, **kwargs):
        """Add __init__ keyword argument injections.

        :param kwargs: Dictionary of injections.
        :type kwargs: dict

        :return: Reference ``self``
        """
        self.__instantiator.add_kwargs(**kwargs)
        return self

    def set_kwargs(self, **kwargs):
        """Set __init__ keyword argument injections.

        Existing __init__ keyword argument injections are dropped.

        :param kwargs: Dictionary of injections.
        :type kwargs: dict

        :return: Reference ``self``
        """
        self.__instantiator.set_kwargs(**kwargs)
        return self

    def clear_kwargs(self):
        """Drop __init__ keyword argument injections.

        :return: Reference ``self``
        """
        self.__instantiator.clear_kwargs()
        return self

    @property
    def attributes(self):
        """Return attribute injections."""
        return self.__instantiator.attributes

    def add_attributes(self, **kwargs):
        """Add attribute injections.

        :param args: Tuple of injections.
        :type args: tuple

        :return: Reference ``self``
        """
        self.__instantiator.add_attributes(**kwargs)
        return self

    def set_attributes(self, **kwargs):
        """Set attribute injections.

        Existing attribute injections are dropped.

        :param args: Tuple of injections.
        :type args: tuple

        :return: Reference ``self``
        """
        self.__instantiator.set_attributes(**kwargs)
        return self

    def clear_attributes(self):
        """Drop attribute injections.

        :return: Reference ``self``
        """
        self.__instantiator.clear_attributes()
        return self

    def reset(self):
        """Reset cached instance, if any.

        :rtype: None
        """
        raise NotImplementedError()


cdef class Singleton(BaseSingleton):
    """Singleton provider returns same instance on every call.

    :py:class:`Singleton` provider creates instance once and returns it on
    every call. :py:class:`Singleton` extends :py:class:`Factory`, so, please
    follow :py:class:`Factory` documentation for getting familiar with
    injections syntax.

    Retrieving of provided instance can be performed via calling
    :py:class:`Singleton` object:

    .. code-block:: python

        singleton = Singleton(SomeClass)
        some_object = singleton()

    .. py:attribute:: provided_type

        If provided type is defined, provider checks that providing class is
        its subclass.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Provided type.
        :type provides: type

        :param args: Tuple of positional argument injections.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword argument injections.
        :type kwargs: dict[str, object]
        """
        self.__storage = None
        super(Singleton, self).__init__(provides, *args, **kwargs)

    def reset(self):
        """Reset cached instance, if any.

        :rtype: None
        """
        self.__storage = None

    cpdef object _provide(self, tuple args, dict kwargs):
        """Return single instance."""
        if self.__storage is None:
            self.__storage = __factory_call(self.__instantiator,
                                            args, kwargs)
        return self.__storage


cdef class DelegatedSingleton(Singleton):
    """Delegated singleton is injected "as is".

    .. py:attribute:: provided_type

        If provided type is defined, provider checks that providing class is
        its subclass.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    __IS_DELEGATED__ = True


cdef class ThreadSafeSingleton(BaseSingleton):
    """Thread-safe singleton provider."""

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Provided type.
        :type provides: type

        :param args: Tuple of positional argument injections.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword argument injections.
        :type kwargs: dict[str, object]
        """
        self.__storage = None
        self.__lock = GLOBAL_LOCK
        super(ThreadSafeSingleton, self).__init__(provides, *args, **kwargs)

    def reset(self):
        """Reset cached instance, if any.

        :rtype: None
        """
        self.__storage = None

    cpdef object _provide(self, tuple args, dict kwargs):
        """Return single instance."""
        with self.__lock:
            if self.__storage is None:
                self.__storage = __factory_call(self.__instantiator,
                                                args, kwargs)
        return self.__storage


cdef class DelegatedThreadSafeSingleton(ThreadSafeSingleton):
    """Delegated thread-safe singleton is injected "as is".

    .. py:attribute:: provided_type

        If provided type is defined, provider checks that providing class is
        its subclass.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    __IS_DELEGATED__ = True


cdef class ThreadLocalSingleton(BaseSingleton):
    """Thread-local singleton provides single objects in scope of thread.

    .. py:attribute:: provided_type

        If provided type is defined, provider checks that providing class is
        its subclass.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Provided type.
        :type provides: type

        :param args: Tuple of positional argument injections.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword argument injections.
        :type kwargs: dict[str, object]
        """
        self.__storage = threading.local()
        super(ThreadLocalSingleton, self).__init__(provides, *args, **kwargs)

    def reset(self):
        """Reset cached instance, if any.

        :rtype: None
        """
        self.__storage.instance = None

    cpdef object _provide(self, tuple args, dict kwargs):
        """Return single instance."""
        cdef object instance

        try:
            instance = self.__storage.instance
        except AttributeError:
            instance = __factory_call(self.__instantiator, args, kwargs)
            self.__storage.instance = instance
        finally:
            return instance


cdef class DelegatedThreadLocalSingleton(ThreadLocalSingleton):
    """Delegated thread-local singleton is injected "as is".

    .. py:attribute:: provided_type

        If provided type is defined, provider checks that providing class is
        its subclass.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    __IS_DELEGATED__ = True
