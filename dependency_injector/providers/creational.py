"""Dependency injector creational providers."""

import six

from dependency_injector.providers.callable import Callable
from dependency_injector.injections import Attribute
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
            .args('positional_arg1', 'positional_arg2') \
            .kwargs(keyword_argument1=3, keyword_argument=4)

        # or

        factory = Factory(SomeClass)
        factory.args('positional_arg1', 'positional_arg2')
        factory.kwargs(keyword_argument1=3, keyword_argument=4)


    Attribute injections are defined by using :py:meth:`Factory.attributes`:

    .. code-block:: python

        factory = Factory(SomeClass) \
            .attributes(attribute1=1, attribute2=2)

    Retrieving of provided instance can be performed via calling
    :py:class:`Factory` object:

    .. code-block:: python

        factory = Factory(SomeClass)
        some_object = factory()

    .. py:attribute:: provided_type

        If provided type is defined, :py:class:`Factory` checks that
        :py:attr:`Factory.provides` is subclass of
        :py:attr:`Factory.provided_type`.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    provided_type = None

    __slots__ = ('cls', '_attributes')

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

        self._attributes = tuple()

        super(Factory, self).__init__(provides, *args, **kwargs)

        self.cls = self._provides

    @property
    def injections(self):
        """Read-only tuple of all injections.

        :rtype: tuple[:py:class:`dependency_injector.injections.Injection`]
        """
        return super(Factory, self).injections + self._attributes

    def attributes(self, **kwargs):
        """Add attribute injections.

        :param kwargs: Dictionary of injections.
        :type kwargs: dict

        :return: Reference ``self``
        """
        self._attributes += tuple(Attribute(name, value)
                                  for name, value in six.iteritems(kwargs))
        return self

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        if self._args:
            args = tuple(arg.get_value() for arg in self._args) + args

        for kwarg in self._kwargs:
            if kwarg.name not in kwargs:
                kwargs[kwarg.name] = kwarg.get_value()

        instance = self._provides(*args, **kwargs)

        for attribute in self._attributes:
            setattr(instance, attribute.name, attribute.get_value())

        return instance


class DelegatedFactory(Factory):
    """:py:class:`DelegatedFactory` is a delegated :py:class:`Factory`.

    :py:class:`DelegatedFactory` is a :py:class:`Factory`, that is injected
    "as is".

    .. py:attribute:: provided_type

        If provided type is defined, :py:class:`Factory` checks that
        :py:attr:`Factory.provides` is subclass of
        :py:attr:`Factory.provided_type`.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    __IS_DELEGATED__ = True


class Singleton(Factory):
    """:py:class:`Singleton` provider returns same instance on every call.

    :py:class:`Singleton` provider creates instance once and return it on every
    call. :py:class:`Singleton` extends :py:class:`Factory`, so, please follow
    :py:class:`Factory` documentation to go inside with injections syntax.

    :py:class:`Singleton` is thread-safe and could be used in multithreading
    environment without any negative impact.

    Retrieving of provided instance can be performed via calling
    :py:class:`Singleton` object:

    .. code-block:: python

        singleton = Singleton(SomeClass)
        some_object = singleton()

    .. py:attribute:: provided_type

        If provided type is defined, :py:class:`Factory` checks that
        :py:attr:`Factory.provides` is subclass of
        :py:attr:`Factory.provided_type`.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    __slots__ = ('_instance',)

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Class or other callable that provides object
            for creation.
        :type provides: type | callable
        """
        self._instance = None
        super(Singleton, self).__init__(provides, *args, **kwargs)

    def reset(self):
        """Reset cached instance, if any.

        :rtype: None
        """
        self._instance = None

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        if self._instance:
            return self._instance

        with GLOBAL_LOCK:
            self._instance = super(Singleton, self)._provide(*args, **kwargs)

        return self._instance


class DelegatedSingleton(Singleton):
    """:py:class:`DelegatedSingleton` is a delegated :py:class:`Singleton`.

    :py:class:`DelegatedSingleton` is a :py:class:`Singleton`, that is injected
    "as is".

    .. py:attribute:: provided_type

        If provided type is defined, :py:class:`Factory` checks that
        :py:attr:`Factory.provides` is subclass of
        :py:attr:`Factory.provided_type`.

        :type: type | None

    .. py:attribute:: cls

        Class that provides object.
        Alias for :py:attr:`provides`.

        :type: type
    """

    __IS_DELEGATED__ = True
