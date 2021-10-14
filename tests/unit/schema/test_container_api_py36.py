"""Container API tests for building container from schema."""

import contextlib
import json
import pathlib
import re

import yaml
from dependency_injector import containers, providers, errors
from pytest import raises


def test_from_schema(container: containers.DynamicContainer):
    container.from_schema(
        {
            "version": "1",
            "container": {
                "provider1": {
                    "provider": "Factory",
                    "provides": "list",
                    "args": [1, 2, 3],
                },
                "provider2": {
                    "provider": "Factory",
                    "provides": "dict",
                    "kwargs": {
                        "one": "container.provider1",
                        "two": 2,
                    },
                },
            },
        },
    )

    assert isinstance(container.provider1, providers.Factory)
    assert container.provider1.provides is list
    assert container.provider1.args == (1, 2, 3)

    assert isinstance(container.provider2, providers.Factory)
    assert container.provider2.provides is dict
    assert container.provider2.kwargs == {"one": container.provider1, "two": 2}


def test_from_yaml_schema(container: containers.DynamicContainer, tmp_path: pathlib.Path):
    schema_path = tmp_path / "schema.yml"
    with open(schema_path, "w") as file:
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

    assert isinstance(container.provider1, providers.Factory)
    assert container.provider1.provides == list
    assert container.provider1.args == (1, 2, 3)

    assert isinstance(container.provider2, providers.Factory)
    assert container.provider2.provides is dict
    assert container.provider2.kwargs == {"one": container.provider1, "two": 2}


def test_from_yaml_schema_with_loader(container: containers.DynamicContainer, tmp_path: pathlib.Path):
    schema_path = tmp_path / "schema.yml"
    with open(schema_path, "w") as file:
        file.write("""
        version: "1"
        container:
          provider:
            provider: Factory
            provides: list
            args: [1, 2, 3]
        """)
    container.from_yaml_schema(schema_path, loader=yaml.Loader)

    assert isinstance(container.provider, providers.Factory)
    assert container.provider.provides is list
    assert container.provider.args == (1, 2, 3)


def test_from_yaml_schema_no_yaml_installed(container: containers.DynamicContainer):
    @contextlib.contextmanager
    def no_yaml_module():
        containers.yaml = None
        yield
        containers.yaml = yaml

    error_message = re.escape(
        "Unable to load yaml schema - PyYAML is not installed. "
        "Install PyYAML or install Dependency Injector with yaml extras: "
        "\"pip install dependency-injector[yaml]\""
    )

    with no_yaml_module():
        with raises(errors.Error, match=error_message):
            container.from_yaml_schema("./no-yaml-installed.yml")


def test_from_json_schema(container: containers.DynamicContainer, tmp_path: pathlib.Path):
    schema_path = tmp_path / "schema.json"
    with open(schema_path, "w") as file:
        file.write(
            json.dumps(
                {
                    "version": "1",
                    "container": {
                        "provider1": {
                            "provider": "Factory",
                            "provides": "list",
                            "args": [1, 2, 3],
                        },
                        "provider2": {
                            "provider": "Factory",
                            "provides": "dict",
                            "kwargs": {
                                "one": "container.provider1",
                                "two": 2,
                            },
                        },
                    },
                },
                indent=4,
            ),
        )
    container.from_json_schema(schema_path)

    assert isinstance(container.provider1, providers.Factory)
    assert container.provider1.provides is list
    assert container.provider1.args == (1, 2, 3)

    assert isinstance(container.provider2, providers.Factory)
    assert container.provider2.provides is dict
    assert container.provider2.kwargs == {"one": container.provider1, "two": 2}
