"""Example of dependency injection in Python."""

import logging
import sqlite3

import boto3

import example.main
import example.services

import dependency_injector.containers as containers
import dependency_injector.providers as providers


class IocContainer(containers.DeclarativeContainer):
    """Application IoC container."""

    config = providers.Configuration('config')
    logger = providers.Singleton(logging.Logger, name='example')

    # Gateways

    database_client = providers.Singleton(sqlite3.connect, config.database.dsn)

    s3_client = providers.Singleton(
        boto3.client, 's3',
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key)

    # Services

    users_service = providers.Factory(
        example.services.UsersService,
        db=database_client,
        logger=logger)

    auth_service = providers.Factory(
        example.services.AuthService,
        token_ttl=config.auth.token_ttl,
        db=database_client,
        logger=logger)

    photos_service = providers.Factory(
        example.services.PhotosService,
        db=database_client,
        s3=s3_client,
        logger=logger)

    # Misc

    main = providers.Callable(
        example.main.main,
        users_service=users_service,
        auth_service=auth_service,
        photos_service=photos_service)
