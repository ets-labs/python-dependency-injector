"""Declarative container provider copying with ``@copy()`` decorator."""

import sqlite3
from unittest import mock

from dependency_injector import containers, providers


class Service:
    def __init__(self, db):
        self.db = db


class SourceContainer(containers.DeclarativeContainer):

    database = providers.Singleton(sqlite3.connect, ":memory:")
    service = providers.Factory(Service, db=database)


# Copy ``SourceContainer`` providers into ``DestinationContainer``:
@containers.copy(SourceContainer)
class DestinationContainer(SourceContainer):

    database = providers.Singleton(mock.Mock)


if __name__ == "__main__":
    container = DestinationContainer()

    service = container.service()
    assert isinstance(service.db, mock.Mock)
