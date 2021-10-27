"""Containers module."""

import logging.config
import sqlite3

import boto3
from dependency_injector import containers, providers

from . import services


class Core(containers.DeclarativeContainer):

    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )


class Gateways(containers.DeclarativeContainer):

    config = providers.Configuration()

    database_client = providers.Singleton(
        sqlite3.connect,
        config.database.dsn,
    )

    s3_client = providers.Singleton(
        boto3.client,
        service_name="s3",
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key,
    )


class Services(containers.DeclarativeContainer):

    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    user = providers.Factory(
        services.UserService,
        db=gateways.database_client,
    )

    auth = providers.Factory(
        services.AuthService,
        db=gateways.database_client,
        token_ttl=config.auth.token_ttl.as_int(),
    )

    photo = providers.Factory(
        services.PhotoService,
        db=gateways.database_client,
        s3=gateways.s3_client,
    )


class Application(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    core = providers.Container(
        Core,
        config=config.core,
    )

    gateways = providers.Container(
        Gateways,
        config=config.gateways,
    )

    services = providers.Container(
        Services,
        config=config.services,
        gateways=gateways,
    )
