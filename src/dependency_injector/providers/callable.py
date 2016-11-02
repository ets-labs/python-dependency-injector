"""Dependency injector callable providers."""

import six

from dependency_injector.providers.base import (
    Provider,
    _parse_positional_injections,
    _parse_keyword_injections,
)
from dependency_injector.utils import represent_provider
from dependency_injector.errors import Error


@six.python_2_unicode_compatible
class Callable(Provider):
    r""":py:class:`Callable` provider calls wrapped callable on every call.

    :py:class:`Callable` supports positional and keyword argument injections:

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

    __slots__ = ('provides', 'args', 'kwargs')

    def __init__(self, provides, *args, **kwargs):
        """Initializer.

        :param provides: Wrapped callable.
        :type provides: callable
        """
        if not callable(provides):
            raise Error('Provider {0} expected to get callable, '
                        'got {0}'.format('.'.join((self.__class__.__module__,
                                                   self.__class__.__name__)),
                                         provides))

        self.provides = provides

        self.args = tuple()
        self.kwargs = dict()

        self.add_args(*args)
        self.add_kwargs(**kwargs)

        super(Callable, self).__init__()

    def add_args(self, *args):
        """Add postional argument injections.

        :param args: Tuple of injections.
        :type args: tuple

        :return: Reference ``self``
        """
        self.args += _parse_positional_injections(args)
        return self

    def add_kwargs(self, **kwargs):
        """Add keyword argument injections.

        :param kwargs: Dictionary of injections.
        :type kwargs: dict

        :return: Reference ``self``
        """
        self.kwargs.update(_parse_keyword_injections(kwargs))
        return self

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        if self.args:
            args = tuple(arg.provide_injection() for arg in self.args) + args

        for name, arg in six.iteritems(self.kwargs):
            if name not in kwargs:
                kwargs[name] = arg.provide_injection()

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
    """

    def provide_injection(self):
        """Injection strategy implementation.

        :rtype: object
        """
        return self
