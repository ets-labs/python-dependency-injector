"""Containers module."""

from dependency_injector import containers, providers

from .services import ConfigService


class Core(containers.DeclarativeContainer):
    config = providers.Configuration("config")


class Storage(containers.DeclarativeContainer):
    queue = providers.Singleton(lambda: "Some storage")


class Adapter(containers.DeclarativeContainer):
    core = providers.DependenciesContainer(config=providers.Configuration())
    tinydb = providers.Singleton(
        lambda db_path: f"DB Path=[{db_path}]",
        db_path=core.config.default.db_path,
    )


class Repository(containers.DeclarativeContainer):
    adapter = providers.DependenciesContainer()
    storage = providers.DependenciesContainer()
    site = providers.Singleton(
        lambda adapter, queue: f"Adapter=[{adapter}], queue=[{queue}]",
        adapter=adapter.tinydb,
        queue=storage.queue,
    )


class Service(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()
    config = providers.Singleton(ConfigService, core.config.provider)


class Application(containers.DeclarativeContainer):

    core = providers.Container(Core)
    storage = providers.Container(Storage)
    adapter = providers.Container(Adapter, core=core)
    repository = providers.Container(Repository, adapter=adapter, storage=storage)
    service = providers.Container(Service, core=core)
