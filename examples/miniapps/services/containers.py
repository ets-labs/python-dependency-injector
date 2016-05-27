"""Example of several Dependency Injector IoC containers."""

import sqlite3
import boto.s3.connection
import example.services

from dependency_injector import containers
from dependency_injector import providers


class Platform(containers.DeclarativeContainer):
    """Container of platform service providers."""

    database = providers.Singleton(sqlite3.connect, ':memory:')

    s3 = providers.Singleton(boto.s3.connection.S3Connection,
                             aws_access_key_id='KEY',
                             aws_secret_access_key='SECRET')


class Services(containers.DeclarativeContainer):
    """Container of business service providers."""

    users = providers.Factory(example.services.Users,
                              db=Platform.database)

    photos = providers.Factory(example.services.Photos,
                               db=Platform.database,
                               s3=Platform.s3)

    auth = providers.Factory(example.services.Auth,
                             db=Platform.database,
                             token_ttl=3600)
