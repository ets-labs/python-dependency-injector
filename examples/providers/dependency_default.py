"""`Dependency` provider default example."""

import abc

from dependency_injector import containers, providers


class Cache(metaclass=abc.ABCMeta):
    ...


class InMemoryCache(Cache):
    ...


class Container(containers.DeclarativeContainer):

    cache = providers.Dependency(instance_of=Cache, default=InMemoryCache())


if __name__ == "__main__":
    container = Container()
    cache = container.cache()  # provides InMemoryCache()

    assert isinstance(cache, InMemoryCache)
