"""Boto3 session example."""

import boto3.session
from dependency_injector import containers, providers


class Service:
    def __init__(self, s3_client, sqs_client):
        self.s3_client = s3_client
        self.sqs_client = sqs_client


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    session = providers.Resource(
        boto3.session.Session,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
    )

    s3_client = providers.Resource(
        session.provided.client.call(),
        service_name="s3",
    )

    sqs_client = providers.Resource(
        providers.MethodCaller(session.provided.client),  # Alternative syntax
        service_name="sqs",
    )

    service1 = providers.Factory(
        Service,
        s3_client=s3_client,
        sqs_client=sqs_client,
    )

    service2 = providers.Factory(
        Service,
        s3_client=session.provided.client.call(service_name="s3"),    # Alternative inline syntax
        sqs_client=session.provided.client.call(service_name="sqs"),  # Alternative inline syntax
    )


def main():
    container = Container()
    container.config.aws_access_key_id.from_env("AWS_ACCESS_KEY_ID")
    container.config.aws_secret_access_key.from_env("AWS_SECRET_ACCESS_KEY")
    container.config.aws_session_token.from_env("AWS_SESSION_TOKEN")
    container.init_resources()

    s3_client = container.s3_client()
    print(s3_client)

    sqs_client = container.sqs_client()
    print(sqs_client)

    service1 = container.service1()
    print(service1, service1.s3_client, service1.sqs_client)
    assert service1.s3_client is s3_client
    assert service1.sqs_client is sqs_client

    service2 = container.service2()
    print(service2, service2.s3_client, service2.sqs_client)
    assert service2.s3_client.__class__.__name__ == "S3"
    assert service2.sqs_client.__class__.__name__ == "SQS"


if __name__ == "__main__":
    main()
