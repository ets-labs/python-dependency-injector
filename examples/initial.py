"""Dependency Injector initial example."""

import sys
import sqlite3
import boto.s3.connection

import services

from dependency_injector import catalogs
from dependency_injector import providers
from dependency_injector import injections


class Platform(catalogs.DeclarativeCatalog):
    """Catalog of platform service providers."""

    database = providers.Singleton(sqlite3.connect, ':memory:')

    s3 = providers.Singleton(boto.s3.connection.S3Connection,
                             aws_access_key_id='KEY',
                             aws_secret_access_key='SECRET')


class Services(catalogs.DeclarativeCatalog):
    """Catalog of business service providers."""

    users = providers.Factory(services.Users,
                              db=Platform.database)

    photos = providers.Factory(services.Photos,
                               db=Platform.database,
                               s3=Platform.s3)

    auth = providers.Factory(services.Auth,
                             db=Platform.database,
                             token_ttl=3600)


@injections.inject(users_service=Services.users)
@injections.inject(auth_service=Services.auth)
def main(argv, users_service, auth_service):
    """Main function."""
    login, password, photo_path = argv[1:]

    user = users_service.get_user(login)
    auth_service.authenticate(user, password)

    upload_photo(user, photo_path)


@injections.inject(photos_service=Services.photos)
def upload_photo(user, photo_path, photos_service):
    """Upload photo."""
    photos_service.upload_photo(user['id'], photo_path)


if __name__ == '__main__':
    main(sys.argv)
