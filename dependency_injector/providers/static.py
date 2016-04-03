"""Dependency injector static providers."""

from dependency_injector.providers.base import Static


class Class(Static):
    """:py:class:`Class` returns provided class "as is".

    .. code-block:: python

        cls_provider = Class(object)
        object_cls = cls_provider()
    """


class Object(Static):
    """:py:class:`Object` returns provided object "as is".

    .. code-block:: python

        object_provider = Object(object())
        object_instance = object_provider()
    """


class Function(Static):
    """:py:class:`Function` returns provided function "as is".

    .. code-block:: python

        function_provider = Function(len)
        len_function = function_provider()
    """


class Value(Static):
    """:py:class:`Value` returns provided value "as is".

    .. code-block:: python

        value_provider = Value(31337)
        value = value_provider()
    """
