"""`Configuration` provider values loading example."""

import os

from dependency_injector import containers, providers
from pydantic import BaseSettings, Field

# Emulate environment variables
os.environ["AWS_ACCESS_KEY_ID"] = "KEY"
os.environ["AWS_SECRET_ACCESS_KEY"] = "SECRET"


class AwsSettings(BaseSettings):

    access_key_id: str = Field(env="aws_access_key_id")
    secret_access_key: str = Field(env="aws_secret_access_key")


class Settings(BaseSettings):

    aws: AwsSettings = AwsSettings()
    optional: str = Field(default="default_value")


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()


if __name__ == "__main__":
    container = Container()

    container.config.from_pydantic(Settings())

    assert container.config.aws.access_key_id() == "KEY"
    assert container.config.aws.secret_access_key() == "SECRET"
    assert container.config.optional() == "default_value"
