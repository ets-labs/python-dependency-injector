"""Example hierarchy of cache clients with abstract base class."""


class AbstractCacheClient(object):
    """Abstract cache client."""


class RedisCacheClient(AbstractCacheClient):
    """Cache client implementation based on Redis."""

    def __init__(self, host, port, db):
        """Initialize instance."""
        self.host = host
        self.port = port
        self.db = db


class MemcacheCacheClient(AbstractCacheClient):
    """Cache client implementation based on Memcached."""

    def __init__(self, hosts, port, prefix):
        """Initialize instance."""
        self.hosts = hosts
        self.port = port
        self.prefix = prefix
