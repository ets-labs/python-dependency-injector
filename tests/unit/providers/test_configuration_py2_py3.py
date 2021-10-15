"""Dependency injector config providers unit tests."""

import contextlib
import decimal
import os
import sys
import tempfile

import unittest

from dependency_injector import containers, providers, errors
from pytest import raises
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
        self.config = providers.Configuration(name="config")

    def tearDown(self):
        del self.config

    def test_init_optional(self):
        provider = providers.Configuration()
        provider.set_name("myconfig")
        provider.set_default({"foo": "bar"})
        provider.set_strict(True)

        assert provider.get_name() == "myconfig"
        assert provider.get_default() == {"foo": "bar"}
        assert provider.get_strict() is True

    def test_set_name_returns_self(self):
        provider = providers.Configuration()
        assert provider.set_name("myconfig") is provider

    def test_set_default_returns_self(self):
        provider = providers.Configuration()
        assert provider.set_default({}) is provider

    def test_set_strict_returns_self(self):
        provider = providers.Configuration()
        assert provider.set_strict(True) is provider

    def test_default_name(self):
        config = providers.Configuration()
        assert config.get_name() == "config"

    def test_providers_are_providers(self):
        assert providers.is_provider(self.config.a) is True
        assert providers.is_provider(self.config.a.b) is True
        assert providers.is_provider(self.config.a.b.c) is True
        assert providers.is_provider(self.config.a.b.d) is True

    def test_providers_are_not_delegates(self):
        assert providers.is_delegated(self.config.a) is False
        assert providers.is_delegated(self.config.a.b) is False
        assert providers.is_delegated(self.config.a.b.c) is False
        assert providers.is_delegated(self.config.a.b.d) is False

    def test_providers_identity(self):
        assert self.config.a is self.config.a
        assert self.config.a.b is self.config.a.b
        assert self.config.a.b.c is self.config.a.b.c
        assert self.config.a.b.d is self.config.a.b.d

    def test_get_name(self):
        assert self.config.a.b.c.get_name() == "config.a.b.c"

    def test_providers_value_setting(self):
        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.config.update({"a": {"b": {"c": 1, "d": 2}}})

        assert a() == {"b": {"c": 1, "d": 2}}
        assert ab() == {"c": 1, "d": 2}
        assert abc() == 1
        assert abd() == 2

    def test_providers_with_already_set_value(self):
        self.config.update({"a": {"b": {"c": 1, "d": 2}}})

        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        assert a() == {"b": {"c": 1, "d": 2}}
        assert ab() == {"c": 1, "d": 2}
        assert abc() == 1
        assert abd() == 2

    def test_as_int(self):
        value_provider = providers.Callable(lambda value: value, self.config.test.as_int())
        self.config.from_dict({"test": "123"})

        value = value_provider()
        assert value == 123

    def test_as_float(self):
        value_provider = providers.Callable(lambda value: value, self.config.test.as_float())
        self.config.from_dict({"test": "123.123"})

        value = value_provider()
        assert value == 123.123

    def test_as_(self):
        value_provider = providers.Callable(
            lambda value: value,
            self.config.test.as_(decimal.Decimal),
        )
        self.config.from_dict({"test": "123.123"})

        value = value_provider()
        assert value == decimal.Decimal("123.123")

    @unittest.skipIf(sys.version_info[:2] == (2, 7), "Python 2.7 does not support this assert")
    def test_required(self):
        provider = providers.Callable(
            lambda value: value,
            self.config.a.required(),
        )
        with raises(errors.Error, match="Undefined configuration option \"config.a\""):
            provider()

    def test_required_defined_none(self):
        provider = providers.Callable(
            lambda value: value,
            self.config.a.required(),
        )
        self.config.from_dict({"a": None})
        assert provider() is None

    def test_required_no_side_effect(self):
        _ = providers.Callable(
            lambda value: value,
            self.config.a.required(),
        )
        assert self.config.a() is None

    def test_required_as_(self):
        provider = providers.List(
            self.config.int_test.required().as_int(),
            self.config.float_test.required().as_float(),
            self.config._as_test.required().as_(decimal.Decimal),
        )
        self.config.from_dict({"int_test": "1", "float_test": "2.0", "_as_test": "3.0"})

        assert provider() == [1, 2.0, decimal.Decimal("3.0")]

    def test_providers_value_override(self):
        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        self.config.override({"a": {"b": {"c": 1, "d": 2}}})

        assert a() == {"b": {"c": 1, "d": 2}}
        assert ab() == {"c": 1, "d": 2}
        assert abc() == 1
        assert abd() == 2

    def test_configuration_option_override_and_reset_override(self):
        # Bug: https://github.com/ets-labs/python-dependency-injector/issues/319
        self.config.from_dict({"a": {"b": {"c": 1}}})

        assert self.config.a.b.c() == 1

        with self.config.set("a.b.c", "xxx"):
            assert self.config.a.b.c() == "xxx"
        assert self.config.a.b.c() == 1

        with self.config.a.b.c.override("yyy"):
            assert self.config.a.b.c() == "yyy"

        assert self.config.a.b.c() == 1

    def test_providers_with_already_overridden_value(self):
        self.config.override({"a": {"b": {"c": 1, "d": 2}}})

        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        assert a() == {"b": {"c": 1, "d": 2}}
        assert ab() == {"c": 1, "d": 2}
        assert abc() == 1
        assert abd() == 2

    def test_providers_with_default_value(self):
        self.config = providers.Configuration(name="config", default={"a": {"b": {"c": 1, "d": 2}}})

        a = self.config.a
        ab = self.config.a.b
        abc = self.config.a.b.c
        abd = self.config.a.b.d

        assert a() == {"b": {"c": 1, "d": 2}}
        assert ab() == {"c": 1, "d": 2}
        assert abc() == 1
        assert abd() == 2

    def test_providers_with_default_value_overriding(self):
        self.config = providers.Configuration(
            name="config", default={"a": {"b": {"c": 1, "d": 2}}})

        assert self.config.a() == {"b": {"c": 1, "d": 2}}
        assert self.config.a.b() == {"c": 1, "d": 2}
        assert self.config.a.b.c() == 1
        assert self.config.a.b.d() == 2

        self.config.override({"a": {"b": {"c": 3, "d": 4}}})
        assert self.config.a() == {"b": {"c": 3, "d": 4}}
        assert self.config.a.b() == {"c": 3, "d": 4}
        assert self.config.a.b.c() == 3
        assert self.config.a.b.d() == 4

        self.config.reset_override()
        assert self.config.a() == {"b": {"c": 1, "d": 2}}
        assert self.config.a.b() == {"c": 1, "d": 2}
        assert self.config.a.b.c() == 1
        assert self.config.a.b.d() == 2

    def test_value_of_undefined_option(self):
        assert self.config.a() is None

    @unittest.skipIf(sys.version_info[:2] == (2, 7), "Python 2.7 does not support this assert")
    def test_value_of_undefined_option_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(errors.Error, match="Undefined configuration option \"config.a\""):
            self.config.a()

    @unittest.skipIf(sys.version_info[:2] == (2, 7), "Python 2.7 does not support this assert")
    def test_value_of_undefined_option_with_root_none_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.override(None)
        with raises(errors.Error, match="Undefined configuration option \"config.a\""):
            self.config.a()

    def test_value_of_defined_none_option_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_dict({"a": None})
        assert self.config.a() is None

    def test_getting_of_special_attributes(self):
        with raises(AttributeError):
            self.config.__name__

    def test_getting_of_special_attributes_from_child(self):
        a = self.config.a
        with raises(AttributeError):
            a.__name__

    def test_context_manager_alias(self):
        class Container(containers.DeclarativeContainer):
            config = providers.Configuration()

        container = Container()

        with container.config as cfg:
            cfg.override({"foo": "foo", "bar": "bar"})

        assert container.config() == {"foo": "foo", "bar": "bar"}
        assert cfg() == {"foo": "foo", "bar": "bar"}
        assert container.config is cfg

    def test_option_context_manager_alias(self):
        class Container(containers.DeclarativeContainer):
            config = providers.Configuration()

        container = Container()

        with container.config.option as opt:
            opt.override({"foo": "foo", "bar": "bar"})

        assert container.config() == {"option": {"foo": "foo", "bar": "bar"}}
        assert container.config.option() == {"foo": "foo", "bar": "bar"}
        assert opt() == {"foo": "foo", "bar": "bar"}
        assert container.config.option is opt

    def test_missing_key(self):
        # See: https://github.com/ets-labs/python-dependency-injector/issues/358
        self.config.override(None)
        value = self.config.key()
        assert value is None

    def test_deepcopy(self):
        provider = providers.Configuration("config")
        provider_copy = providers.deepcopy(provider)

        assert provider is not provider_copy
        assert isinstance(provider, providers.Configuration)

    def test_deepcopy_from_memo(self):
        provider = providers.Configuration("config")
        provider_copy_memo = providers.Configuration("config")

        provider_copy = providers.deepcopy(provider, memo={id(provider): provider_copy_memo})

        assert provider_copy is provider_copy_memo

    def test_deepcopy_overridden(self):
        provider = providers.Configuration("config")
        object_provider = providers.Object(object())

        provider.override(object_provider)

        provider_copy = providers.deepcopy(provider)
        object_provider_copy = provider_copy.overridden[0]

        assert provider is not provider_copy
        assert isinstance(provider, providers.Configuration)

        assert object_provider is not object_provider_copy
        assert isinstance(object_provider_copy, providers.Object)

    def test_repr(self):
        assert repr(self.config) == (
            "<dependency_injector.providers."
            "Configuration({0}) at {1}>".format(repr("config"), hex(id(self.config)))
        )

    def test_repr_child(self):
        assert repr(self.config.a.b.c) == (
            "<dependency_injector.providers."
            "ConfigurationOption({0}) at {1}>".format(repr("config.a.b.c"), hex(id(self.config.a.b.c)))
        )


class ConfigLinkingTests(unittest.TestCase):

    class TestCore(containers.DeclarativeContainer):
        config = providers.Configuration("core")
        value_getter = providers.Callable(lambda _: _, config.value)

    class TestServices(containers.DeclarativeContainer):
        config = providers.Configuration("services")
        value_getter = providers.Callable(lambda _: _, config.value)

    def test(self):
        root_config = providers.Configuration("main")
        core = self.TestCore(config=root_config.core)
        services = self.TestServices(config=root_config.services)

        root_config.override(
            {
                "core": {
                    "value": "core",
                },
                "services": {
                    "value": "services",
                },
            },
        )

        assert core.config() == {"value": "core"}
        assert core.config.value() == "core"
        assert core.value_getter() == "core"

        assert services.config() == {"value": "services"}
        assert services.config.value() == "services"
        assert services.value_getter() == "services"

    def test_double_override(self):
        root_config = providers.Configuration("main")
        core = self.TestCore(config=root_config.core)
        services = self.TestServices(config=root_config.services)

        root_config.override(
            {
                "core": {
                    "value": "core1",
                },
                "services": {
                    "value": "services1",
                },
            },
        )
        root_config.override(
            {
                "core": {
                    "value": "core2",
                },
                "services": {
                    "value": "services2",
                },
            },
        )

        assert core.config() == {"value": "core2"}
        assert core.config.value() == "core2"
        assert core.value_getter() == "core2"

        assert services.config() == {"value": "services2"}
        assert services.config.value() == "services2"
        assert services.value_getter() == "services2"

    def test_reset_overriding_cache(self):
        # See: https://github.com/ets-labs/python-dependency-injector/issues/428
        class Core(containers.DeclarativeContainer):
            config = providers.Configuration()

            greetings = providers.Factory(str, config.greeting)

        class Application(containers.DeclarativeContainer):
            config = providers.Configuration()

            core = providers.Container(
                Core,
                config=config,
            )

            greetings = providers.Factory(str, config.greeting)

        container = Application()

        container.config.set("greeting", "Hello World")
        assert container.greetings() == "Hello World"
        assert container.core.greetings() == "Hello World"

        container.config.set("greeting", "Hello Bob")
        assert container.greetings() == "Hello Bob"
        assert container.core.greetings() == "Hello Bob"

    def test_reset_overriding_cache_for_option(self):
        # See: https://github.com/ets-labs/python-dependency-injector/issues/428
        class Core(containers.DeclarativeContainer):
            config = providers.Configuration()

            greetings = providers.Factory(str, config.greeting)

        class Application(containers.DeclarativeContainer):
            config = providers.Configuration()

            core = providers.Container(
                Core,
                config=config.option,
            )

            greetings = providers.Factory(str, config.option.greeting)

        container = Application()

        container.config.set("option.greeting", "Hello World")
        assert container.greetings() == "Hello World"
        assert container.core.greetings() == "Hello World"

        container.config.set("option.greeting", "Hello Bob")
        assert container.greetings() == "Hello Bob"
        assert container.core.greetings() == "Hello Bob"


class ConfigFromIniTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name="config")

        _, self.config_file_1 = tempfile.mkstemp()
        with open(self.config_file_1, "w") as config_file:
            config_file.write(
                "[section1]\n"
                "value1=1\n"
                "\n"
                "[section2]\n"
                "value2=2\n"
            )

        _, self.config_file_2 = tempfile.mkstemp()
        with open(self.config_file_2, "w") as config_file:
            config_file.write(
                "[section1]\n"
                "value1=11\n"
                "value11=11\n"
                "[section3]\n"
                "value3=3\n"
            )

    def tearDown(self):
        del self.config
        os.unlink(self.config_file_1)
        os.unlink(self.config_file_2)

    def test(self):
        self.config.from_ini(self.config_file_1)

        assert self.config() == {"section1": {"value1": "1"}, "section2": {"value2": "2"}}
        assert self.config.section1() == {"value1": "1"}
        assert self.config.section1.value1() == "1"
        assert self.config.section2() == {"value2": "2"}
        assert self.config.section2.value2() == "2"

    def test_option(self):
        self.config.option.from_ini(self.config_file_1)

        assert self.config() == {"option": {"section1": {"value1": "1"}, "section2": {"value2": "2"}}}
        assert self.config.option() == {"section1": {"value1": "1"}, "section2": {"value2": "2"}}
        assert self.config.option.section1() == {"value1": "1"}
        assert self.config.option.section1.value1() == "1"
        assert self.config.option.section2() == {"value2": "2"}
        assert self.config.option.section2.value2() == "2"

    def test_merge(self):
        self.config.from_ini(self.config_file_1)
        self.config.from_ini(self.config_file_2)

        assert self.config() == {
            "section1": {
                "value1": "11",
                "value11": "11",
            },
            "section2": {
                "value2": "2",
            },
            "section3": {
                "value3": "3",
            },
        }
        assert self.config.section1() == {"value1": "11", "value11": "11"}
        assert self.config.section1.value1() == "11"
        assert self.config.section1.value11() == "11"
        assert self.config.section2() == {"value2": "2"}
        assert self.config.section2.value2() == "2"
        assert self.config.section3() == {"value3": "3"}
        assert self.config.section3.value3() == "3"

    def test_file_does_not_exist(self):
        self.config.from_ini("./does_not_exist.ini")
        assert self.config() == {}

    def test_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(IOError):
            self.config.from_ini("./does_not_exist.ini")

    def test_option_file_does_not_exist(self):
        self.config.option.from_ini("does_not_exist.ini")
        assert self.config.option.undefined() is None

    def test_option_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(IOError):
            self.config.option.from_ini("./does_not_exist.ini")

    def test_required_file_does_not_exist(self):
        with raises(IOError):
            self.config.from_ini("./does_not_exist.ini", required=True)

    def test_required_option_file_does_not_exist(self):
        with raises(IOError):
            self.config.option.from_ini("./does_not_exist.ini", required=True)

    def test_not_required_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_ini("./does_not_exist.ini", required=False)
        assert self.config() == {}

    def test_not_required_option_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_ini("./does_not_exist.ini", required=False)
        with raises(errors.Error):
            self.config.option()


class ConfigFromIniWithEnvInterpolationTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name="config")

        os.environ["CONFIG_TEST_ENV"] = "test-value"
        os.environ["CONFIG_TEST_PATH"] = "test-path"

        _, self.config_file = tempfile.mkstemp()
        with open(self.config_file, "w") as config_file:
            config_file.write(
                "[section1]\n"
                "value1=${CONFIG_TEST_ENV}\n"
                "value2=${CONFIG_TEST_PATH}/path\n"
            )

    def tearDown(self):
        del self.config
        os.environ.pop("CONFIG_TEST_ENV", None)
        os.environ.pop("CONFIG_TEST_PATH", None)
        os.unlink(self.config_file)

    def test_env_variable_interpolation(self):
        self.config.from_ini(self.config_file)

        assert self.config() == {
            "section1": {
                "value1": "test-value",
                "value2": "test-path/path",
            },
        }
        assert self.config.section1() == {
            "value1": "test-value",
            "value2": "test-path/path",
        }
        assert self.config.section1.value1() == "test-value"
        assert self.config.section1.value2() == "test-path/path"

    def test_missing_envs_not_required(self):
        del os.environ["CONFIG_TEST_ENV"]
        del os.environ["CONFIG_TEST_PATH"]

        self.config.from_ini(self.config_file)

        assert self.config() == {
            "section1": {
                "value1": "",
                "value2": "/path",
            },
        }
        assert self.config.section1() == {
            "value1": "",
            "value2": "/path",
        }
        assert self.config.section1.value1() == ""
        assert self.config.section1.value2() == "/path"

    def test_missing_envs_required(self):
        with open(self.config_file, "w") as config_file:
            config_file.write(
                "[section]\n"
                "undefined=${UNDEFINED}\n"
            )

        with raises(ValueError) as exception_info:
            self.config.from_ini(self.config_file, envs_required=True)
        assert str(exception_info.value) == "Missing required environment variable \"UNDEFINED\""

    def test_missing_envs_strict_mode(self):
        with open(self.config_file, "w") as config_file:
            config_file.write(
                "[section]\n"
                "undefined=${UNDEFINED}\n"
            )

        self.config.set_strict(True)
        with raises(ValueError) as exception_info:
            self.config.from_ini(self.config_file)
        assert str(exception_info.value) == "Missing required environment variable \"UNDEFINED\""

    def test_option_missing_envs_not_required(self):
        del os.environ["CONFIG_TEST_ENV"]
        del os.environ["CONFIG_TEST_PATH"]

        self.config.option.from_ini(self.config_file)

        assert self.config.option() == {
            "section1": {
                "value1": "",
                "value2": "/path",
            },
        }
        assert self.config.option.section1() == {
            "value1": "",
            "value2": "/path",
        }
        assert self.config.option.section1.value1() == ""
        assert self.config.option.section1.value2() == "/path"

    def test_option_missing_envs_required(self):
        with open(self.config_file, "w") as config_file:
            config_file.write(
                "[section]\n"
                "undefined=${UNDEFINED}\n"
            )

        with raises(ValueError) as exception_info:
            self.config.option.from_ini(self.config_file, envs_required=True)
        assert str(exception_info.value) == "Missing required environment variable \"UNDEFINED\""

    def test_option_missing_envs_strict_mode(self):
        with open(self.config_file, "w") as config_file:
            config_file.write(
                "[section]\n"
                "undefined=${UNDEFINED}\n"
            )

        self.config.set_strict(True)
        with raises(ValueError) as exception_info:
            self.config.option.from_ini(self.config_file)
        assert str(exception_info.value) == "Missing required environment variable \"UNDEFINED\""

    def test_default_values(self):
        os.environ["DEFINED"] = "defined"
        self.addCleanup(os.environ.pop, "DEFINED")

        with open(self.config_file, "w") as config_file:
            config_file.write(
                "[section]\n"
                "defined_with_default=${DEFINED:default}\n"
                "undefined_with_default=${UNDEFINED:default}\n"
                "complex=${DEFINED}/path/${DEFINED:default}/${UNDEFINED}/${UNDEFINED:default}\n"
            )

        self.config.from_ini(self.config_file)

        assert self.config.section() == {
            "defined_with_default": "defined",
            "undefined_with_default": "default",
            "complex": "defined/path/defined//default",
        }


class ConfigFromYamlTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name="config")

        _, self.config_file_1 = tempfile.mkstemp()
        with open(self.config_file_1, "w") as config_file:
            config_file.write(
                "section1:\n"
                "  value1: 1\n"
                "\n"
                "section2:\n"
                "  value2: 2\n"
            )

        _, self.config_file_2 = tempfile.mkstemp()
        with open(self.config_file_2, "w") as config_file:
            config_file.write(
                "section1:\n"
                "  value1: 11\n"
                "  value11: 11\n"
                "section3:\n"
                "  value3: 3\n"
            )

    def tearDown(self):
        del self.config
        os.unlink(self.config_file_1)
        os.unlink(self.config_file_2)

    def test(self):
        self.config.from_yaml(self.config_file_1)

        assert self.config() == {"section1": {"value1": 1}, "section2": {"value2": 2}}
        assert self.config.section1() == {"value1": 1}
        assert self.config.section1.value1() == 1
        assert self.config.section2() == {"value2": 2}
        assert self.config.section2.value2() == 2

    def test_merge(self):
        self.config.from_yaml(self.config_file_1)
        self.config.from_yaml(self.config_file_2)

        assert self.config() == {
            "section1": {
                "value1": 11,
                "value11": 11,
            },
            "section2": {
                "value2": 2,
            },
            "section3": {
                "value3": 3,
            },
        }
        assert self.config.section1() == {"value1": 11, "value11": 11}
        assert self.config.section1.value1() == 11
        assert self.config.section1.value11() == 11
        assert self.config.section2() == {"value2": 2}
        assert self.config.section2.value2() == 2
        assert self.config.section3() == {"value3": 3}
        assert self.config.section3.value3() == 3

    def test_file_does_not_exist(self):
        self.config.from_yaml("./does_not_exist.yml")
        assert self.config() == {}

    def test_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(IOError):
            self.config.from_yaml("./does_not_exist.yml")

    def test_option_file_does_not_exist(self):
        self.config.option.from_yaml("./does_not_exist.yml")
        assert self.config.option() is None

    def test_option_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(IOError):
            self.config.option.from_yaml("./does_not_exist.yml")

    def test_required_file_does_not_exist(self):
        with raises(IOError):
            self.config.from_yaml("./does_not_exist.yml", required=True)

    def test_required_option_file_does_not_exist(self):
        with raises(IOError):
            self.config.option.from_yaml("./does_not_exist.yml", required=True)

    def test_not_required_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_yaml("./does_not_exist.yml", required=False)
        assert self.config() == {}

    def test_not_required_option_file_does_not_exist_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_yaml("./does_not_exist.yml", required=False)
        with raises(errors.Error):
            self.config.option()

    def test_no_yaml_installed(self):
        @contextlib.contextmanager
        def no_yaml_module():
            yaml = providers.yaml
            providers.yaml = None

            yield

            providers.yaml = yaml

        with no_yaml_module():
            with raises(errors.Error) as error:
                self.config.from_yaml(self.config_file_1)

        assert error.value.args[0] == (
            "Unable to load yaml configuration - PyYAML is not installed. "
            "Install PyYAML or install Dependency Injector with yaml extras: "
            "\"pip install dependency-injector[yaml]\""
        )

    def test_option_no_yaml_installed(self):
        @contextlib.contextmanager
        def no_yaml_module():
            yaml = providers.yaml
            providers.yaml = None

            yield

            providers.yaml = yaml

        with no_yaml_module():
            with raises(errors.Error) as error:
                self.config.option.from_yaml(self.config_file_1)

        assert error.value.args[0] == (
            "Unable to load yaml configuration - PyYAML is not installed. "
            "Install PyYAML or install Dependency Injector with yaml extras: "
            "\"pip install dependency-injector[yaml]\""
        )


class ConfigFromYamlWithEnvInterpolationTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name="config")

        os.environ["CONFIG_TEST_ENV"] = "test-value"
        os.environ["CONFIG_TEST_PATH"] = "test-path"

        _, self.config_file = tempfile.mkstemp()
        with open(self.config_file, "w") as config_file:
            config_file.write(
                "section1:\n"
                "  value1: ${CONFIG_TEST_ENV}\n"
                "  value2: ${CONFIG_TEST_PATH}/path\n"
            )

    def tearDown(self):
        del self.config
        os.environ.pop("CONFIG_TEST_ENV", None)
        os.environ.pop("CONFIG_TEST_PATH", None)
        os.unlink(self.config_file)

    def test_env_variable_interpolation(self):
        self.config.from_yaml(self.config_file)

        assert self.config() == {
            "section1": {
                "value1": "test-value",
                "value2": "test-path/path",
            },
        }
        assert self.config.section1() == {
            "value1": "test-value",
            "value2": "test-path/path",
        }
        assert self.config.section1.value1() == "test-value"
        assert self.config.section1.value2() == "test-path/path"

    def test_missing_envs_not_required(self):
        del os.environ["CONFIG_TEST_ENV"]
        del os.environ["CONFIG_TEST_PATH"]

        self.config.from_yaml(self.config_file)

        assert self.config() == {
            "section1": {
                "value1": None,
                "value2": "/path",
            },
        }
        assert self.config.section1() == {
            "value1": None,
            "value2": "/path",
        }
        assert self.config.section1.value1() is None
        assert self.config.section1.value2() == "/path"

    def test_missing_envs_required(self):
        with open(self.config_file, "w") as config_file:
            config_file.write(
                "section:\n"
                "  undefined: ${UNDEFINED}\n"
            )

        with raises(ValueError) as context:
            self.config.from_yaml(self.config_file, envs_required=True)
        assert str(context.value) == "Missing required environment variable \"UNDEFINED\""

    def test_missing_envs_strict_mode(self):
        with open(self.config_file, "w") as config_file:
            config_file.write(
                "section:\n"
                "  undefined: ${UNDEFINED}\n"
            )

        self.config.set_strict(True)
        with raises(ValueError) as context:
            self.config.from_yaml(self.config_file)
        assert str(context.value) == "Missing required environment variable \"UNDEFINED\""

    def test_option_missing_envs_not_required(self):
        del os.environ["CONFIG_TEST_ENV"]
        del os.environ["CONFIG_TEST_PATH"]

        self.config.option.from_yaml(self.config_file)

        assert self.config.option() == {
            "section1": {
                "value1": None,
                "value2": "/path",
            },
        }
        assert self.config.option.section1() == {
            "value1": None,
            "value2": "/path",
        }
        assert self.config.option.section1.value1() is None
        assert self.config.option.section1.value2() == "/path"

    def test_option_missing_envs_required(self):
        with open(self.config_file, "w") as config_file:
            config_file.write(
                "section:\n"
                "  undefined: ${UNDEFINED}\n"
            )

        with raises(ValueError) as context:
            self.config.option.from_yaml(self.config_file, envs_required=True)
        assert str(context.value) == "Missing required environment variable \"UNDEFINED\""

    def test_option_missing_envs_strict_mode(self):
        with open(self.config_file, "w") as config_file:
            config_file.write(
                "section:\n"
                "  undefined: ${UNDEFINED}\n"
            )

        self.config.set_strict(True)
        with raises(ValueError) as context:
            self.config.option.from_yaml(self.config_file)
        assert str(context.value) == "Missing required environment variable \"UNDEFINED\""

    def test_default_values(self):
        os.environ["DEFINED"] = "defined"
        self.addCleanup(os.environ.pop, "DEFINED")

        with open(self.config_file, "w") as config_file:
            config_file.write(
                "section:\n"
                "  defined_with_default: ${DEFINED:default}\n"
                "  undefined_with_default: ${UNDEFINED:default}\n"
                "  complex: ${DEFINED}/path/${DEFINED:default}/${UNDEFINED}/${UNDEFINED:default}\n"
            )

        self.config.from_yaml(self.config_file)

        assert self.config.section() == {
            "defined_with_default": "defined",
            "undefined_with_default": "default",
            "complex": "defined/path/defined//default",
        }

    def test_option_env_variable_interpolation(self):
        self.config.option.from_yaml(self.config_file)

        assert self.config.option() == {
            "section1": {
                "value1": "test-value",
                "value2": "test-path/path",
            },
        }
        assert self.config.option.section1() == {
            "value1": "test-value",
            "value2": "test-path/path",
        }
        assert self.config.option.section1.value1() == "test-value"
        assert self.config.option.section1.value2() == "test-path/path"

    def test_env_variable_interpolation_custom_loader(self):
        self.config.from_yaml(self.config_file, loader=yaml.UnsafeLoader)

        assert self.config.section1() == {
            "value1": "test-value",
            "value2": "test-path/path",
        }
        assert self.config.section1.value1() == "test-value"
        assert self.config.section1.value2() == "test-path/path"

    def test_option_env_variable_interpolation_custom_loader(self):
        self.config.option.from_yaml(self.config_file, loader=yaml.UnsafeLoader)

        assert self.config.option.section1() == {
            "value1": "test-value",
            "value2": "test-path/path",
        }
        assert self.config.option.section1.value1() == "test-value"
        assert self.config.option.section1.value2() == "test-path/path"


class ConfigFromPydanticTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name="config")

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

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test(self):
        self.config.from_pydantic(self.Settings1())

        assert self.config() == {"section1": {"value1": 1}, "section2": {"value2": 2}}
        assert self.config.section1() == {"value1": 1}
        assert self.config.section1.value1() == 1
        assert self.config.section2() == {"value2": 2}
        assert self.config.section2.value2() == 2

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_kwarg(self):
        self.config.from_pydantic(self.Settings1(), exclude={"section2"})

        assert self.config() == {"section1": {"value1": 1}}
        assert self.config.section1() == {"value1": 1}
        assert self.config.section1.value1() == 1

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_merge(self):
        self.config.from_pydantic(self.Settings1())
        self.config.from_pydantic(self.Settings2())

        assert self.config() == {
            "section1": {
                "value1": 11,
                "value11": 11,
            },
            "section2": {
                "value2": 2,
            },
            "section3": {
                "value3": 3,
            },
        }
        assert self.config.section1() == {"value1": 11, "value11": 11}
        assert self.config.section1.value1() == 11
        assert self.config.section1.value11() == 11
        assert self.config.section2() == {"value2": 2}
        assert self.config.section2.value2() == 2
        assert self.config.section3() == {"value3": 3}
        assert self.config.section3.value3() == 3

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_empty_settings(self):
        self.config.from_pydantic(pydantic.BaseSettings())
        assert self.config() == {}

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_empty_settings_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(ValueError):
            self.config.from_pydantic(pydantic.BaseSettings())

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_option_empty_settings(self):
        self.config.option.from_pydantic(pydantic.BaseSettings())
        assert self.config.option() == {}

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_option_empty_settings_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(ValueError):
            self.config.option.from_pydantic(pydantic.BaseSettings())

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_required_empty_settings(self):
        with raises(ValueError):
            self.config.from_pydantic(pydantic.BaseSettings(), required=True)

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_required_option_empty_settings(self):
        with raises(ValueError):
            self.config.option.from_pydantic(pydantic.BaseSettings(), required=True)

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_not_required_empty_settings_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_pydantic(pydantic.BaseSettings(), required=False)
        assert self.config() == {}

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_not_required_option_empty_settings_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_pydantic(pydantic.BaseSettings(), required=False)
        assert self.config.option() == {}
        assert self.config() == {"option": {}}

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_not_instance_of_settings(self):
        with raises(errors.Error) as error:
            self.config.from_pydantic({})

        assert error.value.args[0] == (
            "Unable to recognize settings instance, expect \"pydantic.BaseSettings\", "
            "got {0} instead".format({})
        )

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_option_not_instance_of_settings(self):
        with raises(errors.Error) as error:
            self.config.option.from_pydantic({})

        assert error.value.args[0] == (
            "Unable to recognize settings instance, expect \"pydantic.BaseSettings\", "
            "got {0} instead".format({})
        )

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_subclass_instead_of_instance(self):
        with raises(errors.Error) as error:
            self.config.from_pydantic(self.Settings1)

        assert error.value.args[0] == (
            "Got settings class, but expect instance: "
            "instead \"Settings1\" use \"Settings1()\""
        )

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_option_subclass_instead_of_instance(self):
        with raises(errors.Error) as error:
            self.config.option.from_pydantic(self.Settings1)

        assert error.value.args[0] == (
            "Got settings class, but expect instance: "
            "instead \"Settings1\" use \"Settings1()\""
        )

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_no_pydantic_installed(self):
        @contextlib.contextmanager
        def no_pydantic_module():
            pydantic = providers.pydantic
            providers.pydantic = None

            yield

            providers.pydantic = pydantic

        with no_pydantic_module():
            with raises(errors.Error) as error:
                self.config.from_pydantic(self.Settings1())

        assert error.value.args[0] == (
            "Unable to load pydantic configuration - pydantic is not installed. "
            "Install pydantic or install Dependency Injector with pydantic extras: "
            "\"pip install dependency-injector[pydantic]\""
        )

    @unittest.skipIf(sys.version_info[:2] < (3, 6), "Pydantic supports Python 3.6+")
    def test_option_no_pydantic_installed(self):
        @contextlib.contextmanager
        def no_pydantic_module():
            pydantic = providers.pydantic
            providers.pydantic = None

            yield

            providers.pydantic = pydantic

        with no_pydantic_module():
            with raises(errors.Error) as error:
                self.config.option.from_pydantic(self.Settings1())

        assert error.value.args[0] == (
            "Unable to load pydantic configuration - pydantic is not installed. "
            "Install pydantic or install Dependency Injector with pydantic extras: "
            "\"pip install dependency-injector[pydantic]\""
        )


class ConfigFromDict(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name="config")

        self.config_options_1 = {
            "section1": {
                "value1": "1",
            },
            "section2": {
                "value2": "2",
            },
        }
        self.config_options_2 = {
            "section1": {
                "value1": "11",
                "value11": "11",
            },
            "section3": {
                "value3": "3",
            },
        }

    def test(self):
        self.config.from_dict(self.config_options_1)

        assert self.config() == {"section1": {"value1": "1"}, "section2": {"value2": "2"}}
        assert self.config.section1() == {"value1": "1"}
        assert self.config.section1.value1() == "1"
        assert self.config.section2() == {"value2": "2"}
        assert self.config.section2.value2() == "2"

    def test_merge(self):
        self.config.from_dict(self.config_options_1)
        self.config.from_dict(self.config_options_2)

        assert self.config() == {
            "section1": {
                "value1": "11",
                "value11": "11",
            },
            "section2": {
                "value2": "2",
            },
            "section3": {
                "value3": "3",
            },
        }
        assert self.config.section1() == {"value1": "11", "value11": "11"}
        assert self.config.section1.value1() == "11"
        assert self.config.section1.value11() == "11"
        assert self.config.section2() == {"value2": "2"}
        assert self.config.section2.value2() == "2"
        assert self.config.section3() == {"value3": "3"}
        assert self.config.section3.value3() == "3"

    def test_empty_dict(self):
        self.config.from_dict({})
        assert self.config() == {}

    def test_option_empty_dict(self):
        self.config.option.from_dict({})
        assert self.config.option() == {}

    def test_empty_dict_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(ValueError):
            self.config.from_dict({})

    def test_option_empty_dict_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(ValueError):
            self.config.option.from_dict({})

    def test_required_empty_dict(self):
        with raises(ValueError):
            self.config.from_dict({}, required=True)

    def test_required_option_empty_dict(self):
        with raises(ValueError):
            self.config.option.from_dict({}, required=True)

    def test_not_required_empty_dict_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_dict({}, required=False)
        assert self.config() == {}

    def test_not_required_option_empty_dict_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_dict({}, required=False)
        assert self.config.option() == {}
        assert self.config() == {"option": {}}


class ConfigFromEnvTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name="config")
        os.environ["CONFIG_TEST_ENV"] = "test-value"

    def tearDown(self):
        del self.config
        del os.environ["CONFIG_TEST_ENV"]

    def test(self):
        self.config.from_env("CONFIG_TEST_ENV")
        assert self.config() == "test-value"

    def test_with_children(self):
        self.config.section1.value1.from_env("CONFIG_TEST_ENV")

        assert self.config() == {"section1": {"value1": "test-value"}}
        assert self.config.section1() == {"value1": "test-value"}
        assert self.config.section1.value1() == "test-value"

    def test_default(self):
        self.config.from_env("UNDEFINED_ENV", "default-value")
        assert self.config() == "default-value"

    def test_default_none(self):
        self.config.from_env("UNDEFINED_ENV")
        assert self.config() is None

    def test_option_default_none(self):
        self.config.option.from_env("UNDEFINED_ENV")
        assert self.config.option() is None

    def test_undefined_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(ValueError):
            self.config.from_env("UNDEFINED_ENV")

    def test_option_undefined_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        with raises(ValueError):
            self.config.option.from_env("UNDEFINED_ENV")

    def test_undefined_in_strict_mode_with_default(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_env("UNDEFINED_ENV", "default-value")
        assert self.config() == "default-value"

    def test_option_undefined_in_strict_mode_with_default(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_env("UNDEFINED_ENV", "default-value")
        assert self.config.option() == "default-value"

    def test_required_undefined(self):
        with raises(ValueError):
            self.config.from_env("UNDEFINED_ENV", required=True)

    def test_required_undefined_with_default(self):
        self.config.from_env("UNDEFINED_ENV", default="default-value", required=True)
        assert self.config() == "default-value"

    def test_option_required_undefined(self):
        with raises(ValueError):
            self.config.option.from_env("UNDEFINED_ENV", required=True)

    def test_option_required_undefined_with_default(self):
        self.config.option.from_env("UNDEFINED_ENV", default="default-value", required=True)
        assert self.config.option() == "default-value"

    def test_not_required_undefined_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_env("UNDEFINED_ENV", required=False)
        assert self.config() is None

    def test_option_not_required_undefined_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_env("UNDEFINED_ENV", required=False)
        assert self.config.option() is None

    def test_not_required_undefined_with_default_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.from_env("UNDEFINED_ENV", default="default-value", required=False)
        assert self.config() == "default-value"

    def test_option_not_required_undefined_with_default_in_strict_mode(self):
        self.config = providers.Configuration(strict=True)
        self.config.option.from_env("UNDEFINED_ENV", default="default-value", required=False)
        assert self.config.option() == "default-value"


class ConfigFromValueTests(unittest.TestCase):

    def setUp(self):
        self.config = providers.Configuration(name="config")

    def test_from_value(self):
        test_value = 123321
        self.config.from_value(test_value)
        assert self.config() == test_value

    def test_option_from_value(self):
        test_value_1 = 123
        test_value_2 = 321

        self.config.option1.from_value(test_value_1)
        self.config.option2.from_value(test_value_2)

        assert self.config() == {"option1": test_value_1, "option2": test_value_2}
        assert self.config.option1() == test_value_1
        assert self.config.option2() == test_value_2
