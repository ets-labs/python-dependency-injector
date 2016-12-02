"""Example of dependency injection in Python."""

import logging
import sqlite3

import boto.s3.connection

import example.main
import example.services

import dependency_injector.containers as containers
import dependency_injector.providers as providers


class Platform(containers.DeclarativeContainer):
    """IoC container of platform service providers."""

    configuration = providers.Configuration('config')

    logger = providers.Singleton(logging.Logger, name='example')

    database = providers.Singleton(sqlite3.connect, configuration.database.dsn)

    s3 = providers.Singleton(boto.s3.connection.S3Connection,
                             configuration.aws.access_key_id,
                             configuration.aws.secret_access_key)


class Services(containers.DeclarativeContainer):
    """IoC container of business service providers."""

    users = providers.Factory(example.services.UsersService,
                              logger=Platform.logger,
                              db=Platform.database)

    auth = providers.Factory(example.services.AuthService,
                             logger=Platform.logger,
                             db=Platform.database,
                             token_ttl=Platform.configuration.auth.token_ttl)

    photos = providers.Factory(example.services.PhotosService,
                               logger=Platform.logger,
                               db=Platform.database,
                               s3=Platform.s3)


class Application(containers.DeclarativeContainer):
    """IoC container of application component providers."""

    main = providers.Callable(example.main.main,
                              users_service=Services.users,
                              auth_service=Services.auth,
                              photos_service=Services.photos)
