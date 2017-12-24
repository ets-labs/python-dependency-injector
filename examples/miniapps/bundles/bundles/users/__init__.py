"""Users bundle."""

from dependency_injector import containers
from dependency_injector import providers

from . import entities
from . import repositories


class Users(containers.DeclarativeContainer):
    """Users bundle container."""

    database = providers.Dependency()

    user = providers.Factory(entities.User)
    user_repository = providers.Singleton(repositories.UserRepository,
                                          object_factory=user.provider,
                                          db=database)
