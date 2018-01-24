"""Run 'Bundles' example application."""

import sqlite3
import boto3

from dependency_injector import containers
from dependency_injector import providers

from bundles.users import Users
from bundles.photos import Photos


class Core(containers.DeclarativeContainer):
    """Core container."""

    config = providers.Configuration('config')
    sqlite = providers.Singleton(sqlite3.connect, config.database.dsn)
    s3 = providers.Singleton(
        boto3.client, 's3',
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key)


if __name__ == '__main__':
    # Initializing containers
    core = Core(config={'database': {'dsn': ':memory:'},
                        'aws': {'access_key_id': 'KEY',
                                'secret_access_key': 'SECRET'}})
    users = Users(database=core.sqlite)
    photos = Photos(database=core.sqlite, file_storage=core.s3)

    # Fetching few users
    user_repository = users.user_repository()
    user1 = user_repository.get(id=1)
    user2 = user_repository.get(id=2)

    # Making some checks
    assert user1.id == 1
    assert user2.id == 2
    assert user_repository.db is core.sqlite()
