"""Dependency injector callable providers."""

import six

from dependency_injector.providers.base import Provider

from dependency_injector.injections import (
    _parse_args_injections,
    _parse_kwargs_injections,
)

from dependency_injector.utils import represent_provider

from dependency_injector.errors import Error


@six.python_2_unicode_compatible
class Callable(Provider):
    """:py:class:`Callable` provider calls wrapped callable on every call.

    :py:class:`Callable` provider provides callable that is called on every
    provider call with some predefined dependency injections.

    :py:class:`Callable` syntax of passing injections is the same like
    :py:class:`Factory` one:

    .. code-block:: python

        # simplified syntax for passing positional and keyword argument
        # injections:
        some_function = Callable(some_function, 'arg1', 'arg2', arg3=3, arg4=4)

        # extended (full) syntax for passing positional and keyword argument
        # injections:
        some_function = Callable(some_function,
                                 injections.Arg(1),
                                 injections.Arg(2),
                                 injections.KwArg('some_arg', 3),
                                 injections.KwArg('other_arg', 4))

    .. py:attribute:: provides

        Provided callable.

        :type: callable

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]
    """

    __slots__ = ('provides', 'args', 'kwargs')

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Wrapped callable.
        :type provides: callable

        :param args: Tuple of injections.
        :type args: tuple

        :param kwargs: Dictionary of injections.
        :type kwargs: dict
        """
        if not callable(provides):
            raise Error('Provider {0} expected to get callable, '
                        'got {0}'.format('.'.join((self.__class__.__module__,
                                                   self.__class__.__name__)),
                                         provides))

        self.provides = provides

        self.args = _parse_args_injections(args)
        self.kwargs = _parse_kwargs_injections(args, kwargs)

        super(Callable, self).__init__()

    @property
    def injections(self):
        """Read-only tuple of all injections.

        :rtype: tuple[:py:class:`dependency_injector.injections.Injection`]
        """
        return self.args + self.kwargs

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        if self.args:
            args = tuple(arg.value for arg in self.args) + args

        for kwarg in self.kwargs:
            if kwarg.name not in kwargs:
                kwargs[kwarg.name] = kwarg.value

        return self.provides(*args, **kwargs)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.provides)

    __repr__ = __str__


class DelegatedCallable(Callable):
    """:py:class:`DelegatedCallable` is a delegated :py:class:`Callable`.

    :py:class:`DelegatedCallable` is a :py:class:`Callable`, that is injected
    "as is".

    .. py:attribute:: provides

        Provided callable.

        :type: callable

    .. py:attribute:: args

        Tuple of positional argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.Arg`]

    .. py:attribute:: kwargs

        Tuple of keyword argument injections.

        :type: tuple[:py:class:`dependency_injector.injections.KwArg`]
    """

    __IS_DELEGATED__ = True
