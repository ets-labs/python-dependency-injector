"""`Configuration` provider values loading example."""

import os

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()


if __name__ == "__main__":
    os.environ.setdefault("ENV_VAR", "default value")

    container = Container()
    container.config.from_yaml("config-with-env-var.yml")

    assert container.config.section.option() == "default value"
