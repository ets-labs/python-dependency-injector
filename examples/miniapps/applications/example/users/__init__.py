"""Users package."""

from core import containers
from core import providers

from . import entities
from . import repositories


class Users(containers.DeclarativeContainer):
    """Users container."""

    database = providers.Dependency()

    user = providers.Factory(entities.User)
    user_repository = providers.Singleton(repositories.UserRepository,
                                          object_factory=user.provider,
                                          db=database)
