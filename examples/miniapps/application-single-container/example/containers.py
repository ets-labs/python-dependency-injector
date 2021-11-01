"""Containers module."""

import logging.config
import sqlite3

import boto3
from dependency_injector import containers, providers

from . import services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    # Gateways

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

    # Services

    user_service = providers.Factory(
        services.UserService,
        db=database_client,
    )

    auth_service = providers.Factory(
        services.AuthService,
        db=database_client,
        token_ttl=config.auth.token_ttl.as_int(),
    )

    photo_service = providers.Factory(
        services.PhotoService,
        db=database_client,
        s3=s3_client,
    )
