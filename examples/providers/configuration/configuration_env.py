"""`Configuration` provider values loading example."""

import os

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()


if __name__ == "__main__":
    container = Container()

    # Emulate environment variables
    os.environ["AWS_ACCESS_KEY_ID"] = "KEY"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "SECRET"

    container.config.aws.access_key_id.from_env("AWS_ACCESS_KEY_ID")
    container.config.aws.secret_access_key.from_env("AWS_SECRET_ACCESS_KEY")
    container.config.optional.from_env("UNDEFINED", "default_value")

    assert container.config.aws.access_key_id() == "KEY"
    assert container.config.aws.secret_access_key() == "SECRET"
    assert container.config.optional() == "default_value"
