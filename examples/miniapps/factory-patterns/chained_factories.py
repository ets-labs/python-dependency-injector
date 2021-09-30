"""`Chained Factories` pattern."""

from dependency_injector import containers, providers


class SqlAlchemyDatabaseService:

    def __init__(self, session, base_class):
        self.session = session
        self.base_class = base_class


class TokensService:

    def __init__(self, id_generator, database):
        self.id_generator = id_generator
        self.database = database


class Token:
    ...


class UsersService:

    def __init__(self, id_generator, database):
        self.id_generator = id_generator
        self.database = database


class User:
    ...


# Sample objects
session = object()
id_generator = object()


class Container(containers.DeclarativeContainer):

    database = providers.Factory(
        SqlAlchemyDatabaseService,
        session=session,
    )

    token_service = providers.Factory(
        TokensService,
        id_generator=id_generator,
        database=providers.Factory(
            database,
            base_class=Token,
        ),
    )

    user_service = providers.Factory(
        UsersService,
        id_generator=id_generator,
        database=providers.Factory(
            database,
            base_class=User,
        ),
    )


if __name__ == "__main__":
    container = Container()

    token_service = container.token_service()
    assert token_service.database.base_class is Token

    user_service = container.user_service()
    assert user_service.database.base_class is User
