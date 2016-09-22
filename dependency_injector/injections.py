"""Dependency injector injections module."""

import warnings

import six

from dependency_injector.providers.base import (
    _parse_positional_injections,
    _parse_keyword_injections,
)
from dependency_injector import utils
from dependency_injector import errors


def inject(*args, **kwargs):
    """Dependency injection decorator.

    .. warning::

        :py:func:`inject` decorator has been deprecated since version 2.2.0.

        Usage of :py:func:`inject` decorator can lead to bad design and could
        be considered as anti-pattern.

    :py:func:`inject` decorator can be used for making inline dependency
    injections. It patches decorated callable in such way that dependency
    injection will be done during every call of decorated callable.

    :py:func:`inject` decorator supports different syntaxes of passing
    injections:

    .. code-block:: python

        # Positional arguments injections:
        @inject(1, 2)
        def some_function(arg1, arg2):
            pass

        # Keyword arguments injections:
        @inject(arg1=1)
        @inject(arg2=2)
        def some_function(arg1, arg2):
            pass

        # Keyword arguments injections into class init:
        @inject(arg1=1)
        @inject(arg2=2)
        class SomeClass(object):

            def __init__(self, arg1, arg2):
                pass

    .. deprecated:: 2.2.0
        Usage of :py:func:`inject` decorator can lead to bad design and could
        be considered as anti-pattern.

    :param args: Tuple of context positional arguments.
    :type args: tuple[object]

    :param kwargs: Dictionary of context keyword arguments.
    :type kwargs: dict[str, object]

    :return: Class / callable decorator
    :rtype: (callable) -> (type | callable)
    """
    warnings.warn(message='Call to a deprecated decorator - @{0}.{1}'
                          .format(inject.__module__, inject.__name__),
                  category=DeprecationWarning,
                  stacklevel=2)

    arg_injections = _parse_positional_injections(args)
    kwarg_injections = _parse_keyword_injections(kwargs)

    def decorator(callback_or_cls):
        """Dependency injection decorator."""
        if isinstance(callback_or_cls, six.class_types):
            cls = callback_or_cls
            cls_init = utils.fetch_cls_init(cls)
            if not cls_init:
                raise errors.Error(
                    'Class {0}.{1} has no __init__() '.format(cls.__module__,
                                                              cls.__name__) +
                    'method and could not be decorated with @inject decorator')
            cls.__init__ = decorator(cls_init)
            return cls

        callback = callback_or_cls

        if hasattr(callback, '__INJECT_DECORATED__'):
            callback.args += arg_injections
            callback.kwargs.update(kwarg_injections)
            return callback

        @six.wraps(callback)
        def decorated(*args, **kwargs):
            """Decorated with dependency injection callback."""
            if decorated.args:
                args = tuple(arg.provide_injection()
                             for arg in decorated.args) + args

            for name, arg in six.iteritems(decorated.kwargs):
                if name not in kwargs:
                    kwargs[name] = arg.provide_injection()

            return callback(*args, **kwargs)

        decorated.__INJECT_DECORATED__ = True
        decorated.origin = callback
        decorated.args = arg_injections
        decorated.kwargs = kwarg_injections

        return decorated
    return decorator
