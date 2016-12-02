"""Dependency injector configuration providers.

Powered by Cython.
"""

from .base cimport (
    Provider,
)
from .utils cimport (
    represent_provider,
    deepcopy,
)


cdef class Configuration(Provider):
    """Configuration provider.

    Configuration provider helps with implementing late static binding of
    configuration options - use first, set last.

    .. code-block:: python

        config = Configuration('config')

        print(config.section1.option1())  # None
        print(config.section1.option2())  # None

        config.update({'section1': {'option1': 1,
                                    'option2': 2}})

        print(config.section1.option1())  # 1
        print(config.section1.option2())  # 2
    """

    def __init__(self, name):
        """Initializer.

        :param name: Name of configuration unit.
        :type name: str
        """
        self.__name = name
        self.__value = None
        self.__children = dict()
        super(Configuration, self).__init__()

    def __deepcopy__(self, memo):
        """Create and return full copy of provider."""
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__(self.__name)
        copied.update(deepcopy(self.__value))

        for overriding_provider in self.overridden:
            copied.override(deepcopy(overriding_provider, memo))

        return copied

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.__name)

    def __getattr__(self, name):
        """Return child configuration provider."""
        cdef Configuration child_provider
        cdef object value

        child_provider = self.__children.get(name)

        if child_provider is None:
            child_provider = self.__class__(self._get_child_name(name))

            if isinstance(self.__value, dict):
                child_provider.update(self.__value.get(name))

            self.__children[name] = child_provider

        return child_provider

    cpdef str get_name(self):
        """Name of configuration unit."""
        return self.__name

    cpdef object update(self, value):
        """Set configuration options.

        :param value: Value of configuration option.
        :type value: object | dict

        :rtype: None
        """
        cdef Configuration child_provider
        cdef object child_value

        self.__value = value

        if not isinstance(self.__value, dict):
            return

        for name in self.__value:
            child_provider = self.__children.get(name)

            if child_provider is None:
                continue

            child_provider.update(self.__value.get(name))

    cpdef object _provide(self, tuple args, dict kwargs):
        """Return result of provided callable's call."""
        return self.__value

    cpdef str _get_child_name(self, str child_name):
        cdef str child_full_name

        child_full_name = ''

        if self.__name:
            child_full_name += self.__name + '.'

        child_full_name += child_name

        return child_full_name
