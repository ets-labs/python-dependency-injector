"""Dependency injector callable providers.

Powered by Cython.
"""

from dependency_injector.errors import Error

from .base cimport Provider
from .injections cimport (
    PositionalInjection,
    NamedInjection,
    parse_positional_injections,
    parse_named_injections,
)
from .utils cimport (
    represent_provider,
    deepcopy,
)


cdef class Callable(Provider):
    r"""Callable provider calls wrapped callable on every call.

    Callable supports positional and keyword argument injections:

    .. code-block:: python

        some_function = Callable(some_function,
                                 'positional_arg1', 'positional_arg2',
                                 keyword_argument1=3, keyword_argument=4)

        # or

        some_function = Callable(some_function) \
            .add_args('positional_arg1', 'positional_arg2') \
            .add_kwargs(keyword_argument1=3, keyword_argument=4)

        # or

        some_function = Callable(some_function)
        some_function.add_args('positional_arg1', 'positional_arg2')
        some_function.add_kwargs(keyword_argument1=3, keyword_argument=4)
    """

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Wrapped callable.
        :type provides: callable

        :param args: Tuple of positional argument injections.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword argument injections.
        :type kwargs: dict[str, object]
        """
        if not callable(provides):
            raise Error('Provider {0} expected to get callable, '
                        'got {0}'.format('.'.join((self.__class__.__module__,
                                                   self.__class__.__name__)),
                                         provides))
        self.__provides = provides

        self.__args = tuple()
        self.__args_len = 0
        self.set_args(*args)

        self.__kwargs = tuple()
        self.__kwargs_len = 0
        self.set_kwargs(**kwargs)

        super(Callable, self).__init__()

    def __deepcopy__(self, memo):
        """Create and return full copy of provider."""
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__(self.provides,
                                *deepcopy(self.args, memo),
                                **deepcopy(self.kwargs, memo))

        for overriding_provider in self.overridden:
            copied.override(deepcopy(overriding_provider, memo))

        return copied

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.__provides)

    @property
    def provides(self):
        """Return wrapped callable."""
        return self.__provides

    @property
    def args(self):
        """Return positional argument injections."""
        cdef int index
        cdef PositionalInjection arg
        cdef list args

        args = list()
        for index in range(self.__args_len):
            arg = self.__args[index]
            args.append(arg.__value)
        return tuple(args)

    def add_args(self, *args):
        """Add postional argument injections.

        :param args: Tuple of injections.
        :type args: tuple

        :return: Reference ``self``
        """
        self.__args += parse_positional_injections(args)
        self.__args_len = len(self.__args)
        return self

    def set_args(self, *args):
        """Set postional argument injections.

        Existing positional argument injections are dropped.

        :param args: Tuple of injections.
        :type args: tuple

        :return: Reference ``self``
        """
        self.__args = parse_positional_injections(args)
        self.__args_len = len(self.__args)
        return self

    def clear_args(self):
        """Drop postional argument injections.

        :return: Reference ``self``
        """
        self.__args = tuple()
        self.__args_len = len(self.__args)
        return self

    @property
    def kwargs(self):
        """Return keyword argument injections."""
        cdef int index
        cdef NamedInjection kwarg
        cdef dict kwargs

        kwargs = dict()
        for index in range(self.__kwargs_len):
            kwarg = self.__kwargs[index]
            kwargs[kwarg.__name] = kwarg.__value
        return kwargs

    def add_kwargs(self, **kwargs):
        """Add keyword argument injections.

        :param kwargs: Dictionary of injections.
        :type kwargs: dict

        :return: Reference ``self``
        """
        self.__kwargs += parse_named_injections(kwargs)
        self.__kwargs_len = len(self.__kwargs)
        return self

    def set_kwargs(self, **kwargs):
        """Set keyword argument injections.

        Existing keyword argument injections are dropped.

        :param kwargs: Dictionary of injections.
        :type kwargs: dict

        :return: Reference ``self``
        """
        self.__kwargs = parse_named_injections(kwargs)
        self.__kwargs_len = len(self.__kwargs)
        return self

    def clear_kwargs(self):
        """Drop keyword argument injections.

        :return: Reference ``self``
        """
        self.__kwargs = tuple()
        self.__kwargs_len = len(self.__kwargs)
        return self

    cpdef object _provide(self, tuple args, dict kwargs):
        """Return result of provided callable's call."""
        return __callable_call(self, args, kwargs)


cdef class DelegatedCallable(Callable):
    """Callable that is injected "as is".

    DelegatedCallable is a :py:class:`Callable`, that is injected "as is".
    """

    __IS_DELEGATED__ = True
