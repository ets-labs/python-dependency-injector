"""Containers module."""

from dependency_injector import containers, providers

from .database import Database
from .repositories import UserRepository
from .services import UserService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.db.url)

    users_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        users_repository=users_repository,
    )
