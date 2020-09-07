"""User containers module."""

from dependency_injector import containers, providers

from . import entities, repositories


class UserContainer(containers.DeclarativeContainer):

    database = providers.Dependency()

    user = providers.Factory(entities.User)

    user_repository = providers.Singleton(
        repositories.UserRepository,
        entity_factory=user.provider,
        db=database,
    )
