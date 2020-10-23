"""`Resource` provider example."""

import concurrent.futures

from dependency_injector import containers, providers


def init_threat_pool(max_workers: int):
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    yield thread_pool
    thread_pool.shutdown(wait=True)


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    thread_pool = providers.Resource(
        init_threat_pool,
        max_workers=config.max_workers,
    )


if __name__ == '__main__':
    container = Container(config={'max_workers': 4})

    container.init_resources()

    thread_pool = container.thread_pool()
    assert list(thread_pool.map(str, range(3))) == ['0', '1', '2']

    container.shutdown_resources()
