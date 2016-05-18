"""Dependency Injector example."""

import sys
import sqlite3

from boto.s3.connection import S3Connection

from dependency_injector import catalogs
from dependency_injector import providers
from dependency_injector import injections

from example import services


class Platform(catalogs.DeclarativeCatalog):
    """Catalog of platform service providers."""

    database = providers.Singleton(sqlite3.connect)
    database.args(':memory:')

    s3 = providers.Singleton(S3Connection)
    s3.kwargs(aws_access_key_id='KEY',
              aws_secret_access_key='SECRET')


class Services(catalogs.DeclarativeCatalog):
    """Catalog of business service providers."""

    users = providers.Factory(services.Users)
    users.kwargs(db=Platform.database)

    photos = providers.Factory(services.Photos)
    photos.kwargs(db=Platform.database,
                  s3=Platform.s3)

    auth = providers.Factory(services.Auth)
    auth.kwargs(db=Platform.database,
                token_ttl=3600)


@injections.inject(users_service=Services.users)
@injections.inject(auth_service=Services.auth)
@injections.inject(photos_service=Services.photos)
def main(argv, users_service, auth_service, photos_service):
    """Main function."""
    login, password, photo_path = argv[1:]

    user = users_service.get_user(login)
    auth_service.authenticate(user, password)
    photos_service.upload_photo(user['id'], photo_path)


if __name__ == '__main__':
    main(sys.argv)
