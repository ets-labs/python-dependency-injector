import contextlib
import json
import os.path
import tempfile
import unittest

import yaml
from dependency_injector import containers, providers, errors


class FromSchemaTests(unittest.TestCase):

    def test(self):
        container = containers.DynamicContainer()
        container.from_schema(
            {
                'version': '1',
                'container': {
                    'provider1': {
                        'provider': 'Factory',
                        'provides': 'list',
                        'args': [1, 2, 3],
                    },
                    'provider2': {
                        'provider': 'Factory',
                        'provides': 'dict',
                        'kwargs': {
                            'one': 'container.provider1',
                            'two': 2,
                        },
                    },
                },
            },
        )

        self.assertIsInstance(container.provider1, providers.Factory)
        self.assertIs(container.provider1.provides, list)
        self.assertEqual(container.provider1.args, (1, 2, 3))

        self.assertIsInstance(container.provider2, providers.Factory)
        self.assertIs(container.provider2.provides, dict)
        self.assertEqual(container.provider2.kwargs, {'one': container.provider1, 'two': 2})


class FromYamlSchemaTests(unittest.TestCase):

    def test(self):
        container = containers.DynamicContainer()

        with tempfile.TemporaryDirectory() as tmp_dir:
            schema_path = os.path.join(tmp_dir, 'schema.yml')
            with open(schema_path, 'w') as file:
                file.write("""
                version: "1"
                container:
                  provider1:
                    provider: Factory
                    provides: list
                    args:
                      - 1
                      - 2
                      - 3
                  provider2:
                    provider: Factory
                    provides: dict
                    kwargs:
                      one: container.provider1
                      two: 2
                """)

            container.from_yaml_schema(schema_path)

        self.assertIsInstance(container.provider1, providers.Factory)
        self.assertIs(container.provider1.provides, list)
        self.assertEqual(container.provider1.args, (1, 2, 3))

        self.assertIsInstance(container.provider2, providers.Factory)
        self.assertIs(container.provider2.provides, dict)
        self.assertEqual(container.provider2.kwargs, {'one': container.provider1, 'two': 2})

    def test_with_loader(self):
        container = containers.DynamicContainer()

        with tempfile.TemporaryDirectory() as tmp_dir:
            schema_path = os.path.join(tmp_dir, 'schema.yml')
            with open(schema_path, 'w') as file:
                file.write("""
                version: "1"
                container:
                  provider:
                    provider: Factory
                    provides: list
                    args: [1, 2, 3]
                """)

            container.from_yaml_schema(schema_path, loader=yaml.Loader)

        self.assertIsInstance(container.provider, providers.Factory)
        self.assertIs(container.provider.provides, list)
        self.assertEqual(container.provider.args, (1, 2, 3))

    def test_no_yaml_installed(self):
        @contextlib.contextmanager
        def no_yaml_module():
            containers.yaml = None
            yield
            containers.yaml = yaml

        container = containers.DynamicContainer()
        with no_yaml_module():
            with self.assertRaises(errors.Error) as error:
                container.from_yaml_schema('./no-yaml-installed.yml')

        self.assertEqual(
            error.exception.args[0],
            'Unable to load yaml schema - PyYAML is not installed. '
            'Install PyYAML or install Dependency Injector with yaml extras: '
            '"pip install dependency-injector[yaml]"',
        )


class FromJsonSchemaTests(unittest.TestCase):

    def test(self):
        container = containers.DynamicContainer()

        with tempfile.TemporaryDirectory() as tmp_dir:
            schema_path = os.path.join(tmp_dir, 'schema.json')
            with open(schema_path, 'w') as file:
                file.write(
                    json.dumps(
                        {
                            'version': '1',
                            'container': {
                                'provider1': {
                                    'provider': 'Factory',
                                    'provides': 'list',
                                    'args': [1, 2, 3],
                                },
                                'provider2': {
                                    'provider': 'Factory',
                                    'provides': 'dict',
                                    'kwargs': {
                                        'one': 'container.provider1',
                                        'two': 2,
                                    },
                                },
                            },
                        },
                        indent=4,
                    ),
                )

            container.from_json_schema(schema_path)

        self.assertIsInstance(container.provider1, providers.Factory)
        self.assertIs(container.provider1.provides, list)
        self.assertEqual(container.provider1.args, (1, 2, 3))

        self.assertIsInstance(container.provider2, providers.Factory)
        self.assertIs(container.provider2.provides, dict)
        self.assertEqual(container.provider2.kwargs, {'one': container.provider1, 'two': 2})
