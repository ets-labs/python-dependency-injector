"""`Configuration` provider values loading example."""

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()


if __name__ == "__main__":
    container = Container()

    container.config.from_dict(
        {
            "aws": {
                 "access_key_id": "KEY",
                 "secret_access_key": "SECRET",
             },
        },
    )

    assert container.config() == {
        "aws": {
            "access_key_id": "KEY",
            "secret_access_key": "SECRET",
        },
    }
    assert container.config.aws() == {
        "access_key_id": "KEY",
        "secret_access_key": "SECRET",
    }
    assert container.config.aws.access_key_id() == "KEY"
    assert container.config.aws.secret_access_key() == "SECRET"
