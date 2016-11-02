"""Dependency injector creational providers."""

import threading

import six

from dependency_injector.providers.callable import Callable
from dependency_injector.providers.base import _parse_keyword_injections
from dependency_injector.utils import GLOBAL_LOCK
from dependency_injector.errors import Error


class Factory(Callable):
    r""":py:class:`Factory` provider creates new instance on every call.

    :py:class:`Factory` supports positional & keyword argument injections,
    as well as attribute injections.

    Positional and keyword argument injections could be defined like this:

    .. code-block:: python

        factory = Factory(SomeClass,
                          'positional_arg1', 'positional_arg2',
                          keyword_argument1=3, keyword_argument=4)

        # or

        factory = Factory(SomeClass) \
            .add_args('positional_arg1', 'positional_arg2') \
            .add_kwargs(keyword_argument1=3, keyword_argument=4)

        # or

        factory = Factory(SomeClass)
        factory.add_args('positional_arg1', 'positional_arg2')
        factory.add_kwargs(keyword_argument1=3, keyword_argument=4)


    Attribute injections are defined by using :py:meth:`Factory.attributes`:

    .. code-block:: python

        factory = Factory(SomeClass) \
            .add_attributes(attribute1=1, attribute2=2)

    Retrieving of provided instance can be performed via calling
    :py:class:`Factory` object:

    .. code-block:: python

        factory = Factory(SomeClass)
        some_object = factory()

    .. py:attribute:: provided_type

        If provided type is defined, provider checks that providing class is
        its subclass.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    provided_type = None

    __slots__ = ('cls', 'attributes')

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Class or other callable that provides object
            for creation.
        :type provides: type | callable
        """
        if (self.__class__.provided_type and
                not issubclass(provides, self.__class__.provided_type)):
            raise Error('{0} can provide only {1} instances'.format(
                self.__class__, self.__class__.provided_type))

        self.attributes = dict()

        super(Factory, self).__init__(provides, *args, **kwargs)

        self.cls = self.provides

    def add_attributes(self, **kwargs):
        """Add attribute injections.

        :param kwargs: Dictionary of injections.
        :type kwargs: dict

        :return: Reference ``self``
        """
        self.attributes.update(_parse_keyword_injections(kwargs))
        return self

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        instance = super(Factory, self)._provide(*args, **kwargs)

        for name, arg in six.iteritems(self.attributes):
            setattr(instance, name, arg.provide_injection())

        return instance


class DelegatedFactory(Factory):
    """:py:class:`Factory` that is injected "as is".

    .. py:attribute:: provided_type

        If provided type is defined, provider checks that providing class is
        its subclass.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    def provide_injection(self):
        """Injection strategy implementation.

        :rtype: object
        """
        return self


class Singleton(Factory):
    """:py:class:`Singleton` provider returns same instance on every call.

    :py:class:`Singleton` provider creates instance once and returns it on
    every call. :py:class:`Singleton` extends :py:class:`Factory`, so, please
    follow :py:class:`Factory` documentation for getting familiar with
    injections syntax.

    :py:class:`Singleton` is thread-safe and could be used in multithreading
    environment without any negative impact.

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

    __slots__ = ('instance',)

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Class or other callable that provides object
            for creation.
        :type provides: type | callable
        """
        self.instance = None
        super(Singleton, self).__init__(provides, *args, **kwargs)

    def reset(self):
        """Reset cached instance, if any.

        :rtype: None
        """
        self.instance = None

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        with GLOBAL_LOCK:
            if self.instance is None:
                self.instance = super(Singleton, self)._provide(*args,
                                                                **kwargs)
        return self.instance


class DelegatedSingleton(Singleton):
    """:py:class:`Singleton` that is injected "as is".

    .. py:attribute:: provided_type

        If provided type is defined, provider checks that providing class is
        its subclass.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    def provide_injection(self):
        """Injection strategy implementation.

        :rtype: object
        """
        return self


class ThreadLocalSingleton(Factory):
    """:py:class:`ThreadLocalSingleton` is singleton based on thread locals.

    :py:class:`ThreadLocalSingleton` provider creates instance once for each
    thread and returns it on every call. :py:class:`ThreadLocalSingleton`
    extends :py:class:`Factory`, so, please follow :py:class:`Factory`
    documentation for getting familiar with injections syntax.

    :py:class:`ThreadLocalSingleton` is thread-safe and could be used in
    multithreading environment without any negative impact.

    Retrieving of provided instance can be performed via calling
    :py:class:`ThreadLocalSingleton` object:

    .. code-block:: python

        singleton = ThreadLocalSingleton(SomeClass)
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

    __slots__ = ('local_storage',)

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Class or other callable that provides object
            for creation.
        :type provides: type | callable
        """
        self.local_storage = threading.local()
        super(ThreadLocalSingleton, self).__init__(provides, *args, **kwargs)

    def reset(self):
        """Reset cached instance, if any.

        :rtype: None
        """
        self.local_storage.instance = None

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        try:
            instance = self.local_storage.instance
        except AttributeError:
            instance = super(ThreadLocalSingleton, self)._provide(*args,
                                                                  **kwargs)
            self.local_storage.instance = instance
        finally:
            return instance


class DelegatedThreadLocalSingleton(ThreadLocalSingleton):
    """:py:class:`ThreadLocalSingleton` that is injected "as is".

    .. py:attribute:: provided_type

        If provided type is defined, provider checks that providing class is
        its subclass.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    def provide_injection(self):
        """Injection strategy implementation.

        :rtype: object
        """
        return self
