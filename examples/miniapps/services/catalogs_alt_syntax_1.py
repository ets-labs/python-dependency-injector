"""Example of several Dependency Injector IoC containers.

Alternative injections definition style #1.
"""

import sqlite3
import boto.s3.connection
import example.services

from dependency_injector import catalogs
from dependency_injector import providers


class Platform(catalogs.DeclarativeCatalog):
    """Catalog of platform service providers."""

    database = providers.Singleton(sqlite3.connect) \
        .args(':memory:')

    s3 = providers.Singleton(boto.s3.connection.S3Connection) \
        .kwargs(aws_access_key_id='KEY',
                aws_secret_access_key='SECRET')


class Services(catalogs.DeclarativeCatalog):
    """Catalog of business service providers."""

    users = providers.Factory(example.services.Users) \
        .kwargs(db=Platform.database)

    photos = providers.Factory(example.services.Photos) \
        .kwargs(db=Platform.database,
                s3=Platform.s3)

    auth = providers.Factory(example.services.Auth) \
        .kwargs(db=Platform.database,
                token_ttl=3600)
