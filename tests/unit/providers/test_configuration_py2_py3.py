"""Dependency injector config providers unit tests."""

import contextlib
import decimal
import os
import sys
import tempfile

import unittest2 as unittest

from dependency_injector import containers, providers, errors
try:
    import yaml
except ImportError:
    yaml = None

try:
    import pydantic
except ImportError:
    pydantic = None


class ConfigTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name='config')

    def tearDown(self):
        del self.config

    def test_default_name(self):
        config = providers.Configuration()
        self.assertEqual(config.get_name(), 'config')

    def test_providers_are_providers(self):
        self.assertTrue(providers.is_provider(self.config.a))
        self.assertTrue(providers.is_provider(self.config.a.b))
        self.assertTrue(providers.is_provider(self.config.a.b.c))
        self.assertTrue(providers.is_provider(self.config.a.b.d))

    def test_providers_are_not_delegates(self):
        self.assertFalse(providers.is_delegated(self.config.a))
        self.assertFalse(providers.is_delegated(self.config.a.b))
        self.assertFalse(providers.is_delegated(self.config.a.b.c))
        self.assertFalse(providers.is_delegated(self.config.a.b.d))

    def test_providers_identity(self):
        self.assertIs(self.config.a, self.config.a)
        self.assertIs(self.config.a.b, self.config.a.b)
        self.assertIs(self.config.a.b.c, self.config.a.b.c)
        self.assertIs(self.config.a.b.d, self.config.a.b.d)

    def test_get_name(self):
        self.assertEqual(self.config.a.b.c.get_name(), 'config.a.b.c')

    def test_providers_value_setting(self):
        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.config.update({'a': {'b': {'c': 1, 'd': 2}}})

        self.assertEqual(a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(ab(), {'c': 1, 'd': 2})
        self.assertEqual(abc(), 1)
        self.assertEqual(abd(), 2)

    def test_providers_with_already_set_value(self):
        self.config.update({'a': {'b': {'c': 1, 'd': 2}}})

        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.assertEqual(a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(ab(), {'c': 1, 'd': 2})
        self.assertEqual(abc(), 1)
        self.assertEqual(abd(), 2)

    def test_as_int(self):
        value_provider = providers.Callable(lambda value: value, self.config.test.as_int())
        self.config.from_dict({'test': '123'})

        value = value_provider()

        self.assertEqual(value, 123)

    def test_as_float(self):
        value_provider = providers.Callable(lambda value: value, self.config.test.as_float())
        self.config.from_dict({'test': '123.123'})

        value = value_provider()

        self.assertEqual(value, 123.123)

    def test_as_(self):
        value_provider = providers.Callable(
            lambda value: value,
            self.config.test.as_(decimal.Decimal),
        )
        self.config.from_dict({'test': '123.123'})

        value = value_provider()

        self.assertEqual(value, decimal.Decimal('123.123'))

    def test_required(self):
        provider = providers.Callable(
            lambda value: value,
            self.config.a.required(),
        )
        with self.assertRaisesRegex(errors.Error, 'Undefined configuration option "config.a"'):
            provider()

    def test_required_defined_none(self):
        provider = providers.Callable(
            lambda value: value,
            self.config.a.required(),
        )
        self.config.from_dict({'a': None})
        self.assertIsNone(provider())

    def test_required_no_side_effect(self):
        _ = providers.Callable(
            lambda value: value,
            self.config.a.required(),
        )
        self.assertIsNone(self.config.a())

    def test_required_as_(self):
        provider = providers.List(
            self.config.int_test.required().as_int(),
            self.config.float_test.required().as_float(),
            self.config._as_test.required().as_(decimal.Decimal),
        )
        self.config.from_dict({'int_test': '1', 'float_test': '2.0', '_as_test': '3.0'})

        self.assertEqual(provider(), [1, 2.0, decimal.Decimal('3.0')])

    def test_providers_value_override(self):
        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.config.override({'a': {'b': {'c': 1, 'd': 2}}})

        self.assertEqual(a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(ab(), {'c': 1, 'd': 2})
        self.assertEqual(abc(), 1)
        self.assertEqual(abd(), 2)

    def test_configuration_option_override_and_reset_override(self):
        # Bug: https://github.com/ets-labs/python-dependency-injector/issues/319
        self.config.from_dict({'a': {'b': {'c': 1}}})

        self.assertEqual(self.config.a.b.c(), 1)

        with self.config.set('a.b.c', 'xxx'):
            self.assertEqual(self.config.a.b.c(), 'xxx')
        self.assertEqual(self.config.a.b.c(), 1)

        with self.config.a.b.c.override('yyy'):
            self.assertEqual(self.config.a.b.c(), 'yyy')

        self.assertEqual(self.config.a.b.c(), 1)

    def test_providers_with_already_overridden_value(self):
        self.config.override({'a': {'b': {'c': 1, 'd': 2}}})

        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.assertEqual(a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(ab(), {'c': 1, 'd': 2})
        self.assertEqual(abc(), 1)
        self.assertEqual(abd(), 2)

    def test_providers_with_default_value(self):
        self.config = providers.Configuration(
            name='config', default={'a': {'b': {'c': 1, 'd': 2}}})

        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.assertEqual(a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(ab(), {'c': 1, 'd': 2})
        self.assertEqual(abc(), 1)
        self.assertEqual(abd(), 2)

    def test_providers_with_default_value_overriding(self):
        self.config = providers.Configuration(
            name='config', default={'a': {'b': {'c': 1, 'd': 2}}})

        self.assertEqual(self.config.a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(self.config.a.b(), {'c': 1, 'd': 2})
        self.assertEqual(self.config.a.b.c(), 1)
        self.assertEqual(self.config.a.b.d(), 2)

        self.config.override({'a': {'b': {'c': 3, 'd': 4}}})
        self.assertEqual(self.config.a(), {'b': {'c': 3, 'd': 4}})
        self.assertEqual(self.config.a.b(), {'c': 3, 'd': 4})
        self.assertEqual(self.config.a.b.c(), 3)
        self.assertEqual(self.config.a.b.d(), 4)

        self.config.reset_override()
        self.assertEqual(self.config.a(), {'b': {'c': 1, 'd': 2}})
        self.assertEqual(self.config.a.b(), {'c': 1, 'd': 2})
        self.assertEqual(self.config.a.b.c(), 1)
        self.assertEqual(self.config.a.b.d(), 2)

    def test_value_of_undefined_option(self):
        self.assertIsNone(self.config.a())

    def test_value_of_undefined_option_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaisesRegex(errors.Error, 'Undefined configuration option "config.a"'):
            self.config.a()

    def test_value_of_undefined_option_with_root_none_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.override(None)
        with self.assertRaisesRegex(errors.Error, 'Undefined configuration option "config.a"'):
            self.config.a()

    def test_value_of_defined_none_option_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_dict({'a': None})
        self.assertIsNone(self.config.a())

    def test_getting_of_special_attributes(self):
        with self.assertRaises(AttributeError):
            self.config.__name__

    def test_getting_of_special_attributes_from_child(self):
        a = self.config.a
        with self.assertRaises(AttributeError):
            a.__name__

    def test_missing_key(self):
        # See: https://github.com/ets-labs/python-dependency-injector/issues/358
        self.config.override(None)
        value = self.config.key()

        self.assertIsNone(value)

    def test_deepcopy(self):
        provider = providers.Configuration('config')
        provider_copy = providers.deepcopy(provider)

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Configuration)

    def test_deepcopy_from_memo(self):
        provider = providers.Configuration('config')
        provider_copy_memo = providers.Configuration('config')

        provider_copy = providers.deepcopy(
            provider, memo={id(provider): provider_copy_memo})

        self.assertIs(provider_copy, provider_copy_memo)

    def test_deepcopy_overridden(self):
        provider = providers.Configuration('config')
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        self.assertIsNot(provider, provider_copy)
        self.assertIsInstance(provider, providers.Configuration)

        self.assertIsNot(object_provider, object_provider_copy)
        self.assertIsInstance(object_provider_copy, providers.Object)

    def test_repr(self):
        self.assertEqual(repr(self.config),
                         '<dependency_injector.providers.'
                         'Configuration({0}) at {1}>'.format(
                             repr('config'),
                             hex(id(self.config))))

    def test_repr_child(self):
        self.assertEqual(repr(self.config.a.b.c),
                         '<dependency_injector.providers.'
                         'ConfigurationOption({0}) at {1}>'.format(
                             repr('config.a.b.c'),
                             hex(id(self.config.a.b.c))))


class ConfigLinkingTests(unittest.TestCase):

    class TestCore(containers.DeclarativeContainer):
        config = providers.Configuration('core')
        value_getter = providers.Callable(lambda _: _, config.value)

    class TestServices(containers.DeclarativeContainer):
        config = providers.Configuration('services')
        value_getter = providers.Callable(lambda _: _, config.value)

    def test(self):
        root_config = providers.Configuration('main')
        core = self.TestCore(config=root_config.core)
        services = self.TestServices(config=root_config.services)

        root_config.override(
            {
                'core': {
                    'value': 'core',
                },
                'services': {
                    'value': 'services',
                },
            },
        )

        self.assertEqual(core.config(), {'value': 'core'})
        self.assertEqual(core.config.value(), 'core')
        self.assertEqual(core.value_getter(), 'core')

        self.assertEqual(services.config(), {'value': 'services'})
        self.assertEqual(services.config.value(), 'services')
        self.assertEqual(services.value_getter(), 'services')

    def test_double_override(self):
        root_config = providers.Configuration('main')
        core = self.TestCore(config=root_config.core)
        services = self.TestServices(config=root_config.services)

        root_config.override(
            {
                'core': {
                    'value': 'core1',
                },
                'services': {
                    'value': 'services1',
                },
            },
        )
        root_config.override(
            {
                'core': {
                    'value': 'core2',
                },
                'services': {
                    'value': 'services2',
                },
            },
        )

        self.assertEqual(core.config(), {'value': 'core2'})
        self.assertEqual(core.config.value(), 'core2')
        self.assertEqual(core.value_getter(), 'core2')

        self.assertEqual(services.config(), {'value': 'services2'})
        self.assertEqual(services.config.value(), 'services2')
        self.assertEqual(services.value_getter(), 'services2')


class ConfigFromIniTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name='config')

        _, self.config_file_1 = tempfile.mkstemp()
        with open(self.config_file_1, 'w') as config_file:
            config_file.write(
                '[section1]\n'
                'value1=1\n'
                '\n'
                '[section2]\n'
                'value2=2\n'
            )

        _, self.config_file_2 = tempfile.mkstemp()
        with open(self.config_file_2, 'w') as config_file:
            config_file.write(
                '[section1]\n'
                'value1=11\n'
                'value11=11\n'
                '[section3]\n'
                'value3=3\n'
            )

    def tearDown(self):
        del self.config
        os.unlink(self.config_file_1)
        os.unlink(self.config_file_2)

    def test(self):
        self.config.from_ini(self.config_file_1)

        self.assertEqual(self.config(), {'section1': {'value1': '1'}, 'section2': {'value2': '2'}})
        self.assertEqual(self.config.section1(), {'value1': '1'})
        self.assertEqual(self.config.section1.value1(), '1')
        self.assertEqual(self.config.section2(), {'value2': '2'})
        self.assertEqual(self.config.section2.value2(), '2')

    def test_option(self):
        self.config.option.from_ini(self.config_file_1)

        self.assertEqual(self.config(), {'option': {'section1': {'value1': '1'}, 'section2': {'value2': '2'}}})
        self.assertEqual(self.config.option(), {'section1': {'value1': '1'}, 'section2': {'value2': '2'}})
        self.assertEqual(self.config.option.section1(), {'value1': '1'})
        self.assertEqual(self.config.option.section1.value1(), '1')
        self.assertEqual(self.config.option.section2(), {'value2': '2'})
        self.assertEqual(self.config.option.section2.value2(), '2')

    def test_merge(self):
        self.config.from_ini(self.config_file_1)
        self.config.from_ini(self.config_file_2)

        self.assertEqual(
            self.config(),
            {
                'section1': {
                    'value1': '11',
                    'value11': '11',
                },
                'section2': {
                    'value2': '2',
                },
                'section3': {
                    'value3': '3',
                },
            },
        )
        self.assertEqual(self.config.section1(), {'value1': '11', 'value11': '11'})
        self.assertEqual(self.config.section1.value1(), '11')
        self.assertEqual(self.config.section1.value11(), '11')
        self.assertEqual(self.config.section2(), {'value2': '2'})
        self.assertEqual(self.config.section2.value2(), '2')
        self.assertEqual(self.config.section3(), {'value3': '3'})
        self.assertEqual(self.config.section3.value3(), '3')

    def test_file_does_not_exist(self):
        self.config.from_ini('./does_not_exist.ini')
        self.assertEqual(self.config(), {})

    def test_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaises(IOError):
            self.config.from_ini('./does_not_exist.ini')

    def test_option_file_does_not_exist(self):
        self.config.option.from_ini('does_not_exist.ini')
        self.assertIsNone(self.config.option.undefined())

    def test_option_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaises(IOError):
            self.config.option.from_ini('./does_not_exist.ini')

    def test_required_file_does_not_exist(self):
        with self.assertRaises(IOError):
            self.config.from_ini('./does_not_exist.ini', required=True)

    def test_required_option_file_does_not_exist(self):
        with self.assertRaises(IOError):
            self.config.option.from_ini('./does_not_exist.ini', required=True)

    def test_not_required_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_ini('./does_not_exist.ini', required=False)
        self.assertEqual(self.config(), {})

    def test_not_required_option_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_ini('./does_not_exist.ini', required=False)
        with self.assertRaises(errors.Error):
            self.config.option()


class ConfigFromIniWithEnvInterpolationTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name='config')

        os.environ['CONFIG_TEST_ENV'] = 'test-value'

        _, self.config_file = tempfile.mkstemp()
        with open(self.config_file, 'w') as config_file:
            config_file.write(
                '[section1]\n'
                'value1=${CONFIG_TEST_ENV}\n'
            )

    def tearDown(self):
        del self.config
        del os.environ['CONFIG_TEST_ENV']
        os.unlink(self.config_file)

    def test_env_variable_interpolation(self):
        self.config.from_ini(self.config_file)

        self.assertEqual(
            self.config(),
            {
                'section1': {
                    'value1': 'test-value',
                },
            },
        )
        self.assertEqual(self.config.section1(), {'value1': 'test-value'})
        self.assertEqual(self.config.section1.value1(), 'test-value')


class ConfigFromYamlTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name='config')

        _, self.config_file_1 = tempfile.mkstemp()
        with open(self.config_file_1, 'w') as config_file:
            config_file.write(
                'section1:\n'
                '  value1: 1\n'
                '\n'
                'section2:\n'
                '  value2: 2\n'
            )

        _, self.config_file_2 = tempfile.mkstemp()
        with open(self.config_file_2, 'w') as config_file:
            config_file.write(
                'section1:\n'
                '  value1: 11\n'
                '  value11: 11\n'
                'section3:\n'
                '  value3: 3\n'
            )

    def tearDown(self):
        del self.config
        os.unlink(self.config_file_1)
        os.unlink(self.config_file_2)

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test(self):
        self.config.from_yaml(self.config_file_1)

        self.assertEqual(self.config(), {'section1': {'value1': 1}, 'section2': {'value2': 2}})
        self.assertEqual(self.config.section1(), {'value1': 1})
        self.assertEqual(self.config.section1.value1(), 1)
        self.assertEqual(self.config.section2(), {'value2': 2})
        self.assertEqual(self.config.section2.value2(), 2)

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_merge(self):
        self.config.from_yaml(self.config_file_1)
        self.config.from_yaml(self.config_file_2)

        self.assertEqual(
            self.config(),
            {
                'section1': {
                    'value1': 11,
                    'value11': 11,
                },
                'section2': {
                    'value2': 2,
                },
                'section3': {
                    'value3': 3,
                },
            },
        )
        self.assertEqual(self.config.section1(), {'value1': 11, 'value11': 11})
        self.assertEqual(self.config.section1.value1(), 11)
        self.assertEqual(self.config.section1.value11(), 11)
        self.assertEqual(self.config.section2(), {'value2': 2})
        self.assertEqual(self.config.section2.value2(), 2)
        self.assertEqual(self.config.section3(), {'value3': 3})
        self.assertEqual(self.config.section3.value3(), 3)

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_file_does_not_exist(self):
        self.config.from_yaml('./does_not_exist.yml')
        self.assertEqual(self.config(), {})

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaises(IOError):
            self.config.from_yaml('./does_not_exist.yml')

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_option_file_does_not_exist(self):
        self.config.option.from_yaml('./does_not_exist.yml')
        self.assertIsNone(self.config.option())

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_option_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaises(IOError):
            self.config.option.from_yaml('./does_not_exist.yml')

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_required_file_does_not_exist(self):
        with self.assertRaises(IOError):
            self.config.from_yaml('./does_not_exist.yml', required=True)

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_required_option_file_does_not_exist(self):
        with self.assertRaises(IOError):
            self.config.option.from_yaml('./does_not_exist.yml', required=True)

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_not_required_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_yaml('./does_not_exist.yml', required=False)
        self.assertEqual(self.config(), {})

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_not_required_option_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_yaml('./does_not_exist.yml', required=False)
        with self.assertRaises(errors.Error):
            self.config.option()

    def test_no_yaml_installed(self):
        @contextlib.contextmanager
        def no_yaml_module():
            yaml = providers.yaml
            providers.yaml = None

            yield

            providers.yaml = yaml

        with no_yaml_module():
            with self.assertRaises(errors.Error) as error:
                self.config.from_yaml(self.config_file_1)

        self.assertEqual(
            error.exception.args[0],
            'Unable to load yaml configuration - PyYAML is not installed. '
            'Install PyYAML or install Dependency Injector with yaml extras: '
            '"pip install dependency-injector[yaml]"',
        )

    def test_option_no_yaml_installed(self):
        @contextlib.contextmanager
        def no_yaml_module():
            yaml = providers.yaml
            providers.yaml = None

            yield

            providers.yaml = yaml

        with no_yaml_module():
            with self.assertRaises(errors.Error) as error:
                self.config.option.from_yaml(self.config_file_1)

        self.assertEqual(
            error.exception.args[0],
            'Unable to load yaml configuration - PyYAML is not installed. '
            'Install PyYAML or install Dependency Injector with yaml extras: '
            '"pip install dependency-injector[yaml]"',
        )


class ConfigFromYamlWithEnvInterpolationTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name='config')

        os.environ['CONFIG_TEST_ENV'] = 'test-value'

        _, self.config_file = tempfile.mkstemp()
        with open(self.config_file, 'w') as config_file:
            config_file.write(
                'section1:\n'
                '  value1: ${CONFIG_TEST_ENV}\n'
            )

    def tearDown(self):
        del self.config
        del os.environ['CONFIG_TEST_ENV']
        os.unlink(self.config_file)

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_env_variable_interpolation(self):
        self.config.from_yaml(self.config_file)

        self.assertEqual(
            self.config(),
            {
                'section1': {
                    'value1': 'test-value',
                },
            },
        )
        self.assertEqual(self.config.section1(), {'value1': 'test-value'})
        self.assertEqual(self.config.section1.value1(), 'test-value')

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_option_env_variable_interpolation(self):
        self.config.option.from_yaml(self.config_file)

        self.assertEqual(
            self.config.option(),
            {
                'section1': {
                    'value1': 'test-value',
                },
            },
        )
        self.assertEqual(self.config.option.section1(), {'value1': 'test-value'})
        self.assertEqual(self.config.option.section1.value1(), 'test-value')

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_env_variable_interpolation_custom_loader(self):
        self.config.from_yaml(self.config_file, loader=yaml.UnsafeLoader)

        self.assertEqual(
            self.config(),
            {
                'section1': {
                    'value1': 'test-value',
                },
            },
        )
        self.assertEqual(self.config.section1(), {'value1': 'test-value'})
        self.assertEqual(self.config.section1.value1(), 'test-value')

    @unittest.skipIf(sys.version_info[:2] == (3, 4), 'PyYAML does not support Python 3.4')
    def test_option_env_variable_interpolation_custom_loader(self):
        self.config.option.from_yaml(self.config_file, loader=yaml.UnsafeLoader)

        self.assertEqual(
            self.config.option(),
            {
                'section1': {
                    'value1': 'test-value',
                },
            },
        )
        self.assertEqual(self.config.option.section1(), {'value1': 'test-value'})
        self.assertEqual(self.config.option.section1.value1(), 'test-value')


class ConfigFromPydanticTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name='config')

        class Section11(pydantic.BaseModel):
            value1 = 1

        class Section12(pydantic.BaseModel):
            value2 = 2

        class Settings1(pydantic.BaseSettings):
            section1 = Section11()
            section2 = Section12()

        self.Settings1 = Settings1

        class Section21(pydantic.BaseModel):
            value1 = 11
            value11 = 11

        class Section3(pydantic.BaseModel):
            value3 = 3

        class Settings2(pydantic.BaseSettings):
            section1 = Section21()
            section3 = Section3()

        self.Settings2 = Settings2

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test(self):
        self.config.from_pydantic(self.Settings1())

        self.assertEqual(self.config(), {'section1': {'value1': 1}, 'section2': {'value2': 2}})
        self.assertEqual(self.config.section1(), {'value1': 1})
        self.assertEqual(self.config.section1.value1(), 1)
        self.assertEqual(self.config.section2(), {'value2': 2})
        self.assertEqual(self.config.section2.value2(), 2)

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_kwarg(self):
        self.config.from_pydantic(self.Settings1(), exclude={'section2'})

        self.assertEqual(self.config(), {'section1': {'value1': 1}})
        self.assertEqual(self.config.section1(), {'value1': 1})
        self.assertEqual(self.config.section1.value1(), 1)

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_merge(self):
        self.config.from_pydantic(self.Settings1())
        self.config.from_pydantic(self.Settings2())

        self.assertEqual(
            self.config(),
            {
                'section1': {
                    'value1': 11,
                    'value11': 11,
                },
                'section2': {
                    'value2': 2,
                },
                'section3': {
                    'value3': 3,
                },
            },
        )
        self.assertEqual(self.config.section1(), {'value1': 11, 'value11': 11})
        self.assertEqual(self.config.section1.value1(), 11)
        self.assertEqual(self.config.section1.value11(), 11)
        self.assertEqual(self.config.section2(), {'value2': 2})
        self.assertEqual(self.config.section2.value2(), 2)
        self.assertEqual(self.config.section3(), {'value3': 3})
        self.assertEqual(self.config.section3.value3(), 3)

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_empty_settings(self):
        self.config.from_pydantic(pydantic.BaseSettings())
        self.assertEqual(self.config(), {})

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_empty_settings_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaises(ValueError):
            self.config.from_pydantic(pydantic.BaseSettings())

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_option_empty_settings(self):
        self.config.option.from_pydantic(pydantic.BaseSettings())
        self.assertEqual(self.config.option(), {})

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_option_empty_settings_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaises(ValueError):
            self.config.option.from_pydantic(pydantic.BaseSettings())

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_required_empty_settings(self):
        with self.assertRaises(ValueError):
            self.config.from_pydantic(pydantic.BaseSettings(), required=True)

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_required_option_empty_settings(self):
        with self.assertRaises(ValueError):
            self.config.option.from_pydantic(pydantic.BaseSettings(), required=True)

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_not_required_empty_settings_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_pydantic(pydantic.BaseSettings(), required=False)
        self.assertEqual(self.config(), {})

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_not_required_option_empty_settings_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_pydantic(pydantic.BaseSettings(), required=False)
        self.assertEqual(self.config.option(), {})
        self.assertEqual(self.config(), {'option': {}})

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_not_instance_of_settings(self):
        with self.assertRaises(errors.Error) as error:
            self.config.from_pydantic({})

        self.assertEqual(
            error.exception.args[0],
            'Unable to recognize settings instance, expect "pydantic.BaseSettings", '
            'got {0} instead'.format({})
        )

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_option_not_instance_of_settings(self):
        with self.assertRaises(errors.Error) as error:
            self.config.option.from_pydantic({})

        self.assertEqual(
            error.exception.args[0],
            'Unable to recognize settings instance, expect "pydantic.BaseSettings", '
            'got {0} instead'.format({})
        )

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_subclass_instead_of_instance(self):
        with self.assertRaises(errors.Error) as error:
            self.config.from_pydantic(self.Settings1)

        self.assertEqual(
            error.exception.args[0],
            'Got settings class, but expect instance: '
            'instead "Settings1" use "Settings1()"'
        )

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_option_subclass_instead_of_instance(self):
        with self.assertRaises(errors.Error) as error:
            self.config.option.from_pydantic(self.Settings1)

        self.assertEqual(
            error.exception.args[0],
            'Got settings class, but expect instance: '
            'instead "Settings1" use "Settings1()"'
        )

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_no_pydantic_installed(self):
        @contextlib.contextmanager
        def no_pydantic_module():
            pydantic = providers.pydantic
            providers.pydantic = None

            yield

            providers.pydantic = pydantic

        with no_pydantic_module():
            with self.assertRaises(errors.Error) as error:
                self.config.from_pydantic(self.Settings1())

        self.assertEqual(
            error.exception.args[0],
            'Unable to load pydantic configuration - pydantic is not installed. '
            'Install pydantic or install Dependency Injector with pydantic extras: '
            '"pip install dependency-injector[pydantic]"',
        )

    @unittest.skipIf(sys.version_info[:2] < (3, 6), 'Pydantic supports Python 3.6+')
    def test_option_no_pydantic_installed(self):
        @contextlib.contextmanager
        def no_pydantic_module():
            pydantic = providers.pydantic
            providers.pydantic = None

            yield

            providers.pydantic = pydantic

        with no_pydantic_module():
            with self.assertRaises(errors.Error) as error:
                self.config.option.from_pydantic(self.Settings1())

        self.assertEqual(
            error.exception.args[0],
            'Unable to load pydantic configuration - pydantic is not installed. '
            'Install pydantic or install Dependency Injector with pydantic extras: '
            '"pip install dependency-injector[pydantic]"',
        )


class ConfigFromDict(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name='config')

        self.config_options_1 = {
            'section1': {
                'value1': '1',
            },
            'section2': {
                'value2': '2',
            },
        }
        self.config_options_2 = {
            'section1': {
                'value1': '11',
                'value11': '11',
            },
            'section3': {
                'value3': '3',
            },
        }

    def test(self):
        self.config.from_dict(self.config_options_1)

        self.assertEqual(self.config(), {'section1': {'value1': '1'}, 'section2': {'value2': '2'}})
        self.assertEqual(self.config.section1(), {'value1': '1'})
        self.assertEqual(self.config.section1.value1(), '1')
        self.assertEqual(self.config.section2(), {'value2': '2'})
        self.assertEqual(self.config.section2.value2(), '2')

    def test_merge(self):
        self.config.from_dict(self.config_options_1)
        self.config.from_dict(self.config_options_2)

        self.assertEqual(
            self.config(),
            {
                'section1': {
                    'value1': '11',
                    'value11': '11',
                },
                'section2': {
                    'value2': '2',
                },
                'section3': {
                    'value3': '3',
                },
            },
        )
        self.assertEqual(self.config.section1(), {'value1': '11', 'value11': '11'})
        self.assertEqual(self.config.section1.value1(), '11')
        self.assertEqual(self.config.section1.value11(), '11')
        self.assertEqual(self.config.section2(), {'value2': '2'})
        self.assertEqual(self.config.section2.value2(), '2')
        self.assertEqual(self.config.section3(), {'value3': '3'})
        self.assertEqual(self.config.section3.value3(), '3')

    def test_empty_dict(self):
        self.config.from_dict({})
        self.assertEqual(self.config(), {})

    def test_option_empty_dict(self):
        self.config.option.from_dict({})
        self.assertEqual(self.config.option(), {})

    def test_empty_dict_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaises(ValueError):
            self.config.from_dict({})

    def test_option_empty_dict_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaises(ValueError):
            self.config.option.from_dict({})

    def test_required_empty_dict(self):
        with self.assertRaises(ValueError):
            self.config.from_dict({}, required=True)

    def test_required_option_empty_dict(self):
        with self.assertRaises(ValueError):
            self.config.option.from_dict({}, required=True)

    def test_not_required_empty_dict_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_dict({}, required=False)
        self.assertEqual(self.config(), {})

    def test_not_required_option_empty_dict_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_dict({}, required=False)
        self.assertEqual(self.config.option(), {})
        self.assertEqual(self.config(), {'option': {}})


class ConfigFromEnvTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name='config')
        os.environ['CONFIG_TEST_ENV'] = 'test-value'

    def tearDown(self):
        del self.config
        del os.environ['CONFIG_TEST_ENV']

    def test(self):
        self.config.from_env('CONFIG_TEST_ENV')
        self.assertEqual(self.config(), 'test-value')

    def test_with_children(self):
        self.config.section1.value1.from_env('CONFIG_TEST_ENV')

        self.assertEqual(self.config(), {'section1': {'value1': 'test-value'}})
        self.assertEqual(self.config.section1(), {'value1': 'test-value'})
        self.assertEqual(self.config.section1.value1(), 'test-value')

    def test_default(self):
        self.config.from_env('UNDEFINED_ENV', 'default-value')
        self.assertEqual(self.config(), 'default-value')

    def test_default_none(self):
        self.config.from_env('UNDEFINED_ENV')
        self.assertIsNone(self.config())

    def test_option_default_none(self):
        self.config.option.from_env('UNDEFINED_ENV')
        self.assertIsNone(self.config.option())

    def test_undefined_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaises(ValueError):
            self.config.from_env('UNDEFINED_ENV')

    def test_option_undefined_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with self.assertRaises(ValueError):
            self.config.option.from_env('UNDEFINED_ENV')

    def test_undefined_in_strict_mode_with_default(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_env('UNDEFINED_ENV', 'default-value')
        self.assertEqual(self.config(), 'default-value')

    def test_option_undefined_in_strict_mode_with_default(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_env('UNDEFINED_ENV', 'default-value')
        self.assertEqual(self.config.option(), 'default-value')

    def test_required_undefined(self):
        with self.assertRaises(ValueError):
            self.config.from_env('UNDEFINED_ENV', required=True)

    def test_required_undefined_with_default(self):
        self.config.from_env('UNDEFINED_ENV', default='default-value', required=True)
        self.assertEqual(self.config(), 'default-value')

    def test_option_required_undefined(self):
        with self.assertRaises(ValueError):
            self.config.option.from_env('UNDEFINED_ENV', required=True)

    def test_option_required_undefined_with_default(self):
        self.config.option.from_env('UNDEFINED_ENV', default='default-value', required=True)
        self.assertEqual(self.config.option(), 'default-value')

    def test_not_required_undefined_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_env('UNDEFINED_ENV', required=False)
        self.assertIsNone(self.config())

    def test_option_not_required_undefined_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_env('UNDEFINED_ENV', required=False)
        self.assertIsNone(self.config.option())

    def test_not_required_undefined_with_default_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_env('UNDEFINED_ENV', default='default-value', required=False)
        self.assertEqual(self.config(), 'default-value')

    def test_option_not_required_undefined_with_default_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_env('UNDEFINED_ENV', default='default-value', required=False)
        self.assertEqual(self.config.option(), 'default-value')
