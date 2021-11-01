"""`Configuration` provider values loading example."""

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()


if __name__ == "__main__":
    container = Container()

    container.config.from_yaml("./config.yml")
    container.config.from_yaml("./config.local.yml")

    assert container.config() == {
        "aws": {
            "access_key_id": "LOCAL-KEY",
            "secret_access_key": "LOCAL-SECRET",
        },
    }
    assert container.config.aws() == {
        "access_key_id": "LOCAL-KEY",
        "secret_access_key": "LOCAL-SECRET",
    }
    assert container.config.aws.access_key_id() == "LOCAL-KEY"
    assert container.config.aws.secret_access_key() == "LOCAL-SECRET"
