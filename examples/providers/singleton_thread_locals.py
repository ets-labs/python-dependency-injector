"""`ThreadLocalSingleton` provider example."""

import threading
import queue

from dependency_injector import containers, providers


def put_in_queue(example_object, queue_object):
    queue_object.put(example_object)


class Container(containers.DeclarativeContainer):

    thread_local_object = providers.ThreadLocalSingleton(object)

    queue_provider = providers.ThreadSafeSingleton(queue.Queue)

    put_in_queue = providers.Callable(
        put_in_queue,
        example_object=thread_local_object,
        queue_object=queue_provider,
    )

    thread_factory = providers.Factory(
        threading.Thread,
        target=put_in_queue.provider,
    )


if __name__ == "__main__":
    container = Container()

    n = 10
    threads = []
    for thread_number in range(n):
        threads.append(
            container.thread_factory(name="Thread{0}".format(thread_number)),
        )
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    all_objects = set()
    while not container.queue_provider().empty():
        all_objects.add(container.queue_provider().get())

    assert len(all_objects) == len(threads) == n
    # Queue contains same number of objects as number of threads where
    # thread-local singleton provider was used.
