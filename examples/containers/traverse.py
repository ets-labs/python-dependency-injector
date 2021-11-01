"""Container traversal example."""

from dependency_injector import containers, providers


def init_database():
    return ...


def init_cache():
    return ...


class Service:
    def __init__(self, database, cache):
        self.database = database
        self.cache = cache


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    service = providers.Factory(
        Service,
        database=providers.Resource(
            init_database,
            url=config.database_url,
        ),
        cache=providers.Resource(
            init_cache,
            hosts=config.cache_hosts,
        ),
    )


if __name__ == "__main__":
    container = Container()

    for provider in container.traverse():
        print(provider)

    # <dependency_injector.providers.Configuration("config") at 0x10d37d200>
    # <dependency_injector.providers.Factory(<class "__main__.Service">) at 0x10d3a2820>
    # <dependency_injector.providers.Resource(<function init_database at 0x10bd2cb80>) at 0x10d346b40>
    # <dependency_injector.providers.ConfigurationOption("config.cache_hosts") at 0x10d37d350>
    # <dependency_injector.providers.Resource(<function init_cache at 0x10be373a0>) at 0x10d346bc0>
    # <dependency_injector.providers.ConfigurationOption("config.database_url") at 0x10d37d2e0>
