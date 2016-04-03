"""Dependency injector config providers."""

import six

from dependency_injector.providers.base import Provider

from dependency_injector.errors import Error

from dependency_injector.utils import represent_provider


@six.python_2_unicode_compatible
class Config(Provider):
    """:py:class:`Config` provider provide dict values.

    :py:class:`Config` provider creates :py:class:`ChildConfig` objects for all
    undefined attribute calls. It makes possible to create deferred config
    value providers. It might be useful in cases where it is needed to
    define / pass some configuration in declarative manner, while
    configuration values will be loaded / updated in application's runtime.
    """

    __slots__ = ('value',)

    def __init__(self, value=None):
        """Initializer.

        :param value: Configuration dictionary.
        :type value: dict[str, object]
        """
        if not value:
            value = dict()
        self.value = value
        super(Config, self).__init__()

    def __getattr__(self, item):
        """Return instance of deferred config.

        :param item: Name of configuration option or section.
        :type item: str

        :rtype: :py:class:`ChildConfig`
        """
        return ChildConfig(parents=(item,), root_config=self)

    def _provide(self, paths=None):
        """Return provided instance.

        :param paths: Tuple of pieces of configuration option / section path.
        :type args: tuple[str]

        :rtype: object
        """
        value = self.value
        if paths:
            for path in paths:
                try:
                    value = value[path]
                except KeyError:
                    raise Error('Config key '
                                '"{0}" is undefined'.format('.'.join(paths)))
        return value

    def update_from(self, value):
        """Update current value from another one.

        :param value: Configuration dictionary.
        :type value: dict[str, object]

        :rtype: None
        """
        self.value.update(value)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self, provides=self.value)

    __repr__ = __str__


@six.python_2_unicode_compatible
class ChildConfig(Provider):
    """:py:class:`ChildConfig` provider provides value from :py:class:`Config`.

    :py:class:`ChildConfig` provides value from the root config object
    according to the current path in the config tree.
    """

    __slots__ = ('parents', 'root_config')

    def __init__(self, parents, root_config):
        """Initializer.

        :param parents: Tuple of pieces of configuration option / section
            parent path.
        :type parents: tuple[str]

        :param root_config: Root configuration object.
        :type root_config: :py:class:`Config`
        """
        self.parents = parents
        self.root_config = root_config
        super(ChildConfig, self).__init__()

    def __getattr__(self, item):
        """Return instance of deferred config.

        :param item: Name of configuration option or section.
        :type item: str

        :rtype: :py:class:`ChildConfig`
        """
        return ChildConfig(parents=self.parents + (item,),
                           root_config=self.root_config)

    def _provide(self, *args, **kwargs):
        """Return provided instance.

        :param args: Tuple of context positional arguments.
        :type args: tuple[object]

        :param kwargs: Dictionary of context keyword arguments.
        :type kwargs: dict[str, object]

        :rtype: object
        """
        return self.root_config(self.parents)

    def __str__(self):
        """Return string representation of provider.

        :rtype: str
        """
        return represent_provider(provider=self,
                                  provides='.'.join(self.parents))

    __repr__ = __str__
