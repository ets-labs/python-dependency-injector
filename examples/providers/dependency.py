"""`Dependency` provider example."""

import abc
import dataclasses

from dependency_injector import containers, providers


class DbAdapter(metaclass=abc.ABCMeta):
    ...


class SqliteDbAdapter(DbAdapter):
    ...


class PostgresDbAdapter(DbAdapter):
    ...


@dataclasses.dataclass
class UserService:
    database: DbAdapter


class Container(containers.DeclarativeContainer):

    database = providers.Dependency(instance_of=DbAdapter)

    user_service = providers.Factory(
        UserService,
        database=database,
    )


if __name__ == "__main__":
    container1 = Container(database=providers.Singleton(SqliteDbAdapter))
    container2 = Container(database=providers.Singleton(PostgresDbAdapter))

    assert isinstance(container1.user_service().database, SqliteDbAdapter)
    assert isinstance(container2.user_service().database, PostgresDbAdapter)

    container3 = Container(database=providers.Singleton(object))
    container3.user_service()  # <-- raises error:
    # <object ...> is not an instance of DbAdapter
