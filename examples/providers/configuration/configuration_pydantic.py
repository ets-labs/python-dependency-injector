"""`Configuration` provider values loading example."""

import os

from dependency_injector import containers, providers
from pydantic_settings import BaseSettings, SettingsConfigDict

# Emulate environment variables
os.environ["AWS_ACCESS_KEY_ID"] = "KEY"
os.environ["AWS_SECRET_ACCESS_KEY"] = "SECRET"


class AwsSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="aws_")

    access_key_id: str
    secret_access_key: str


class Settings(BaseSettings):

    aws: AwsSettings = AwsSettings()
    optional: str = "default_value"


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()


if __name__ == "__main__":
    container = Container()

    container.config.from_pydantic(Settings())

    assert container.config.aws.access_key_id() == "KEY"
    assert container.config.aws.secret_access_key() == "SECRET"
    assert container.config.optional() == "default_value"
