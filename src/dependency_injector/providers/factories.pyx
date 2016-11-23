"""Dependency injector factory providers.

Powered by Cython.
"""

from dependency_injector.errors import Error

from .base cimport Provider
from .callables cimport Callable
from .injections cimport (
    NamedInjection,
    parse_named_injections,
)
from .utils cimport (
    represent_provider,
    deepcopy,
)


cdef class Factory(Provider):
    r"""Factory provider creates new instance on every call.

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


    Attribute injections are defined by using
    :py:meth:`Factory.add_attributes`:

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
    """

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

        self.__instantiator = Callable(provides, *args, **kwargs)

        self.__attributes = tuple()
        self.__attributes_len = 0

        super(Factory, self).__init__()

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

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self,
                                  provides=self.__instantiator.provides)

    @property
    def cls(self):
        """Return provided type."""
        return self.__instantiator.provides

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
        cdef int index
        cdef NamedInjection attribute
        cdef dict attributes

        attributes = dict()
        for index in range(self.__attributes_len):
            attribute = self.__attributes[index]
            attributes[attribute.__name] = attribute.__value
        return attributes

    def add_attributes(self, **kwargs):
        """Add attribute injections.

        :param args: Tuple of injections.
        :type args: tuple

        :return: Reference ``self``
        """
        self.__attributes += parse_named_injections(kwargs)
        self.__attributes_len = len(self.__attributes)
        return self

    def set_attributes(self, **kwargs):
        """Set attribute injections.

        Existing attribute injections are dropped.

        :param args: Tuple of injections.
        :type args: tuple

        :return: Reference ``self``
        """
        self.__attributes = parse_named_injections(kwargs)
        self.__attributes_len = len(self.__attributes)
        return self

    def clear_attributes(self):
        """Drop attribute injections.

        :return: Reference ``self``
        """
        self.__attributes = tuple()
        self.__attributes_len = len(self.__attributes)
        return self

    cpdef object _provide(self, tuple args, dict kwargs):
        """Return new instance."""
        return __factory_call(self, args, kwargs)


cdef class DelegatedFactory(Factory):
    """Factory that is injected "as is".

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
