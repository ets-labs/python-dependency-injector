"""`Resource` provider example."""

import sys
import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from dependency_injector import containers, providers


@contextmanager
def init_thread_pool(max_workers: int):
    thread_pool = ThreadPoolExecutor(max_workers=max_workers)
    yield thread_pool
    thread_pool.shutdown(wait=True)


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    thread_pool = providers.Resource(
        init_thread_pool,
        max_workers=config.max_workers,
    )

    logging = providers.Resource(
        logging.basicConfig,
        level=logging.INFO,
        stream=sys.stdout,
    )


if __name__ == "__main__":
    container = Container(config={"max_workers": 4})

    container.init_resources()

    logging.info("Resources are initialized")
    thread_pool = container.thread_pool()
    thread_pool.map(print, range(10))

    container.shutdown_resources()
