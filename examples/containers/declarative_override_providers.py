"""Declarative container provider override example."""

import sqlite3
from unittest import mock

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    database = providers.Singleton(sqlite3.connect, ":memory:")


if __name__ == "__main__":
    container = Container(database=mock.Mock(sqlite3.Connection))

    database = container.database()
    assert isinstance(database, mock.Mock)
