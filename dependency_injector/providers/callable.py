"""Dependency injector callable providers."""

import six

from dependency_injector.providers.base import Provider
from dependency_injector.injections import Arg, KwArg
from dependency_injector.utils import represent_provider
from dependency_injector.errors import Error


@six.python_2_unicode_compatible
class Callable(Provider):
    r""":py:class:`Callable` provider calls wrapped callable on every call.

    :py:class:`Callable` provider provides callable that is called on every
    provider call with some predefined dependency injections.

    :py:class:`Callable` supports positional and keyword argument injections:

    .. code-block:: python

        some_function = Callable(some_function) \
            .args('arg1', 'arg2') \
            .kwargs(arg3=3, arg4=4)
    """

    __slots__ = ('_provides', '_args', '_kwargs')

    def __init__(self, provides):
        """Initializer.

        :param provides: Wrapped callable.
        :type provides: callable
        """
        if not callable(provides):
            raise Error('Provider {0} expected to get callable, '
                        'got {0}'.format('.'.join((self.__class__.__module__,
                                                   self.__class__.__name__)),
                                         provides))

        self._provides = provides
        self._args = tuple()
        self._kwargs = tuple()

        super(Callable, self).__init__()

    @property
    def injections(self):
        """Read-only tuple of all injections.

        :rtype: tuple[:py:class:`dependency_injector.injections.Injection`]
        """
        return self._args + self._kwargs

    def args(self, *args):
        """Add postional argument injections.

        :param args: Tuple of injections.
        :type args: tuple

        :return: Reference ``self``
        """
        self._args += tuple(Arg(value) for value in args)
        return self

    def kwargs(self, **kwargs):
        """Add keyword argument injections.

        :param kwargs: Dictionary of injections.
        :type kwargs: dict

        :return: Reference ``self``
        """
        self._kwargs += tuple(KwArg(name, value)
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
            args = tuple(arg.value for arg in self._args) + args

        for kwarg in self._kwargs:
            if kwarg.name not in kwargs:
                kwargs[kwarg.name] = kwarg.value

        return self._provides(*args, **kwargs)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self._provides)

    __repr__ = __str__


class DelegatedCallable(Callable):
    """:py:class:`DelegatedCallable` is a delegated :py:class:`Callable`.

    :py:class:`DelegatedCallable` is a :py:class:`Callable`, that is injected
    "as is".
    """

    __IS_DELEGATED__ = True
