"""`AbstractFactory` providers example."""

import cache

import dependency_injector.providers as providers


# Define abstract cache client factory:
cache_client_factory = providers.AbstractFactory(cache.AbstractCacheClient)

if __name__ == '__main__':
    # Override abstract factory with redis client factory:
    cache_client_factory.override(
        providers.Factory(
            cache.RedisCacheClient,
            host='localhost',
            port=6379,
            db=0,
        ),
    )
    redis_cache = cache_client_factory()
    print(redis_cache)
    # <cache.RedisCacheClient object at 0x10975bc50>

    # Override abstract factory with memcache client factory:
    cache_client_factory.override(
        providers.Factory(
            cache.MemcacheCacheClient,
            hosts=['10.0.1.1', '10.0.1.2', '10.0.1.3'],
            port=11211,
            prefix='my_app',
        ),
    )
    memcache_cache = cache_client_factory()
    print(memcache_cache)
    # <cache.MemcacheCacheClient object at 0x10975bc90>
