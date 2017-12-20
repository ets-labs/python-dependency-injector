"""Example applications."""

from core import containers, providers

from users import Users
from photos import Photos


class Core(containers.DeclarativeContainer):
    """Core container."""

    pgsql = providers.Singleton(object)
    s3 = providers.Singleton(object)


if __name__ == '__main__':
    # Initializing containers
    core = Core()
    users = Users(database=core.pgsql)
    photos = Photos(database=core.pgsql, file_storage=core.s3)

    # Fetching few users
    user_repository = users.user_repository()
    user1 = user_repository.get(id=1)
    user2 = user_repository.get(id=2)

    # Making some checks
    assert user1.id == 1
    assert user2.id == 2
    assert user_repository.db is core.pgsql()
