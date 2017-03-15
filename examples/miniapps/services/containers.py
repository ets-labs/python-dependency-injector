"""Example of dependency injection in Python."""

import logging
import sqlite3

import boto3

import example.main
import example.services

import dependency_injector.containers as containers
import dependency_injector.providers as providers


class Core(containers.DeclarativeContainer):
    """IoC container of core component providers."""

    config = providers.Configuration('config')

    logger = providers.Singleton(logging.Logger, name='example')


class Gateways(containers.DeclarativeContainer):
    """IoC container of gateway (API clients to remote services) providers."""

    database = providers.Singleton(sqlite3.connect, Core.config.database.dsn)

    s3 = providers.Singleton(
        boto3.client, 's3',
        aws_access_key_id=Core.config.aws.access_key_id,
        aws_secret_access_key=Core.config.aws.secret_access_key)


class Services(containers.DeclarativeContainer):
    """IoC container of business service providers."""

    users = providers.Factory(example.services.UsersService,
                              db=Gateways.database,
                              logger=Core.logger)

    auth = providers.Factory(example.services.AuthService,
                             db=Gateways.database,
                             logger=Core.logger,
                             token_ttl=Core.config.auth.token_ttl)

    photos = providers.Factory(example.services.PhotosService,
                               db=Gateways.database,
                               s3=Gateways.s3,
                               logger=Core.logger)


class Application(containers.DeclarativeContainer):
    """IoC container of application component providers."""

    main = providers.Callable(example.main.main,
                              users_service=Services.users,
                              auth_service=Services.auth,
                              photos_service=Services.photos)
