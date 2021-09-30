"""`Configuration` provider example."""

import boto3
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    s3_client_factory = providers.Factory(
        boto3.client,
        "s3",
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key,
    )


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
    s3_client = container.s3_client_factory()
