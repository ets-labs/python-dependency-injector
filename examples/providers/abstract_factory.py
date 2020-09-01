"""`AbstractFactory` providers example."""

import abc
import dataclasses
import random
from typing import List

from dependency_injector import providers


class AbstractCacheClient(metaclass=abc.ABCMeta):
    ...


@dataclasses.dataclass
class RedisCacheClient(AbstractCacheClient):
    host: str
    port: int
    db: int


@dataclasses.dataclass
class MemcachedCacheClient(AbstractCacheClient):
    hosts: List[str]
    port: int
    prefix: str


@dataclasses.dataclass
class Service:
    cache: AbstractCacheClient


cache_client_factory = providers.AbstractFactory(AbstractCacheClient)
service_factory = providers.Factory(
    Service,
    cache=cache_client_factory,
)


if __name__ == '__main__':
    cache_type = random.choice(['redis', 'memcached', None])

    if cache_type == 'redis':
        cache_client_factory.override(
            providers.Factory(
                RedisCacheClient,
                host='localhost',
                port=6379,
                db=0,
            ),
        )
    elif cache_type == 'memcached':
        cache_client_factory.override(
            providers.Factory(
                MemcachedCacheClient,
                hosts=['10.0.1.1'],
                port=11211,
                prefix='my_app',
            ),
        )

    service = service_factory()
    print(service.cache)
    # The output depends on cache_type variable value.
    #
    # If the value is 'redis':
    # RedisCacheClient(host='localhost', port=6379, db=0)
    #
    # If the value is 'memcached':
    # MemcachedCacheClient(hosts=['10.0.1.1'], port=11211, prefix='my_app')
    #
    # If the value is None:
    # Error: AbstractFactory(<class '__main__.AbstractCacheClient'>) must be
    # overridden before calling
