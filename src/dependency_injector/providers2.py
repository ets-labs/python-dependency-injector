import weakref

from dependency_injector import providers


class ConfigurationOption(providers.Provider):

    UNDEFINED = object()

    def __init__(self, name, root):
        self._name = name
        self._root_ref = weakref.ref(root)
        self._children = {}
        self._cache = self.UNDEFINED
        super().__init__()

    def __deepcopy__(self, memo):
        """Create and return full copy of provider."""
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        root = self._root_ref()
        root_copy = providers.deepcopy(root, memo)

        copied = self.__class__(self._name, root_copy)
        copied._children = providers.deepcopy(self._children, memo)

        return copied

    def __getattr__(self, item):
        child = self._children.get(item)
        if child is None:
            child_name = '.'.join((self._name, item))
            child = ConfigurationOption(child_name, self._root_ref())
            self._children[item] = child
        return child

    def _provide(self, args, kwargs):
        if self._cache is not self.UNDEFINED:
            return self._cache

        root = self._root_ref()
        value = root.get(self._name)
        self._cache = value
        return value

    def override(self, value):
        if isinstance(value, providers.Provider):
            raise providers.Error('Configuration option can only be overridden by a value')
        root = self._root_ref()
        return root.set(self._name, value)

    def reset_last_overriding(self):
        raise providers.Error('Configuration option does not support this method')

    def reset_override(self):
        raise providers.Error('Configuration option does not support this method')

    def reset_cache(self):
        self._cache = self.UNDEFINED
        for child in self._children.values():
            child.reset_cache()

    def update(self, value):
        """Set configuration options.

        .. deprecated:: 3.11

            Use :py:meth:`Configuration.override` instead.

        :param value: Value of configuration option.
        :type value: object | dict

        :rtype: None
        """
        self.override(value)

    def from_ini(self, filepath):
        """Load configuration from the ini file.

        Loaded configuration is merged recursively over existing configuration.

        :param filepath: Path to the configuration file.
        :type filepath: str

        :rtype: None
        """
        parser = _parse_ini_file(filepath)

        config = {}
        for section in parser.sections():
            config[section] = dict(parser.items(section))

        current_config = self.__call__()
        if not current_config:
            current_config = {}
        self.override(merge_dicts(current_config, config))

    def from_yaml(self, filepath):
        """Load configuration from the yaml file.

        Loaded configuration is merged recursively over existing configuration.

        :param filepath: Path to the configuration file.
        :type filepath: str

        :rtype: None
        """
        if yaml is None:
            raise Error(
                'Unable to load yaml configuration - PyYAML is not installed. '
                'Install PyYAML or install Dependency Injector with yaml extras: '
                '"pip install dependency-injector[yaml]"'
            )

        try:
            with open(filepath) as opened_file:
                config = yaml.load(opened_file, yaml.Loader)
        except IOError:
            return

        current_config = self.__call__()
        if not current_config:
            current_config = {}
        self.override(merge_dicts(current_config, config))

    def from_dict(self, options):
        """Load configuration from the dictionary.

        Loaded configuration is merged recursively over existing configuration.

        :param options: Configuration options.
        :type options: dict

        :rtype: None
        """
        current_config = self.__call__()
        if not current_config:
            current_config = {}
        self.override(merge_dicts(current_config, options))

    def from_env(self, name, default=None):
        """Load configuration value from the environment variable.

        :param name: Name of the environment variable.
        :type name: str

        :param default: Default value that is used if environment variable does not exist.
        :type default: str

        :rtype: None
        """
        value = os.getenv(name, default)
        self.override(value)


class Configuration(providers.Object):

    DEFAULT_NAME = 'config'

    def __init__(self, name=DEFAULT_NAME, default=None):
        self._name = name

        value = {}
        if default is not None:
            assert isinstance(default, dict)
            value = default.copy()

        self._children = {}

        super().__init__(value)

    def __deepcopy__(self, memo):
        """Create and return full copy of provider."""
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__(self._name, self.__provides)
        copied._children = providers.deepcopy(self._children, memo)
        self._copy_overridings(copied, memo)

        return copied

    def __getattr__(self, item):
        child = self._children.get(item)
        if child is None:
            child = ConfigurationOption(item, self)
            self._children[item] = child
        return child

    def get_name(self):
        return self._name

    def get(self, selector):
        keys = selector.split('.')
        value = self.__call__()

        while len(keys) > 0:
            key = keys.pop(0)
            value = value.get(key)
            if value is None:
                break

        return value

    def set(self, selector, value):
        keys = selector.split('.')
        original_value = current_value = self.__call__()

        while len(keys) > 0:
            key = keys.pop(0)
            if len(keys) == 0:
                current_value[key] = value
                break
            temp_value = current_value.get(key, {})
            current_value[key] = temp_value
            current_value = temp_value

        return self.override(original_value)

    def override(self, provider):
        context = super().override(provider)
        self.reset_cache()
        return context

    def reset_last_overriding(self):
        super().reset_last_overriding()
        self.reset_cache()

    def reset_override(self):
        super().reset_override()
        self.reset_cache()

    def reset_cache(self):
        for child in self._children.values():
            child.reset_cache()

    def update(self, value):
        """Set configuration options.

        .. deprecated:: 3.11

            Use :py:meth:`Configuration.override` instead.

        :param value: Value of configuration option.
        :type value: object | dict

        :rtype: None
        """
        self.override(value)

    def from_ini(self, filepath):
        """Load configuration from the ini file.

        Loaded configuration is merged recursively over existing configuration.

        :param filepath: Path to the configuration file.
        :type filepath: str

        :rtype: None
        """
        parser = _parse_ini_file(filepath)

        config = {}
        for section in parser.sections():
            config[section] = dict(parser.items(section))

        current_config = self.__call__()
        if not current_config:
            current_config = {}
        self.override(merge_dicts(current_config, config))

    def from_yaml(self, filepath):
        """Load configuration from the yaml file.

        Loaded configuration is merged recursively over existing configuration.

        :param filepath: Path to the configuration file.
        :type filepath: str

        :rtype: None
        """
        if yaml is None:
            raise Error(
                'Unable to load yaml configuration - PyYAML is not installed. '
                'Install PyYAML or install Dependency Injector with yaml extras: '
                '"pip install dependency-injector[yaml]"'
            )

        try:
            with open(filepath) as opened_file:
                config = yaml.load(opened_file, yaml.Loader)
        except IOError:
            return

        current_config = self.__call__()
        if not current_config:
            current_config = {}
        self.override(merge_dicts(current_config, config))

    def from_dict(self, options):
        """Load configuration from the dictionary.

        Loaded configuration is merged recursively over existing configuration.

        :param options: Configuration options.
        :type options: dict

        :rtype: None
        """
        current_config = self.__call__()
        if not current_config:
            current_config = {}
        self.override(merge_dicts(current_config, options))

    def from_env(self, name, default=None):
        """Load configuration value from the environment variable.

        :param name: Name of the environment variable.
        :type name: str

        :param default: Default value that is used if environment variable does not exist.
        :type default: str

        :rtype: None
        """
        value = os.getenv(name, default)
        self.override(value)


if __name__ == '__main__':
    config = Configuration()
    config.override({'a': {'b': 1}, 'c': 2})
    print(config())
    print(config.get('a.b'))

    config.set('x.y.z', 123)
    print(config())
    assert config.get('x.y.z') == 123
    assert config.x.y.z() == 123

    config.set('a.c', 321)
    print(config())
    assert config.get('a.c') == 321
    assert config.a.c() == 321

    config.set('a.b', 111)
    print(config())
    assert config.get('a.b') == 111
    assert config.a.b() == 111
    assert config.get('a') == {'b': 111, 'c': 321}
    assert config.a() == {'b': 111, 'c': 321}

    config = Configuration()

    core_config = Configuration()
    core_config.override(config.core)

    config.override({'core': {'a': {'b': 1}}})

    print(config.core.a.b())
    print(core_config.a.b())
    assert config.core.a.b() == 1
    assert core_config.a.b() == 1

