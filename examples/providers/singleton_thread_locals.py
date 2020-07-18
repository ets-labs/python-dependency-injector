"""`ThreadLocalSingleton` providers example."""

import threading
import queue

import dependency_injector.providers as providers


def example(example_object, queue_object):
    """Put provided object in the provided queue."""
    queue_object.put(example_object)


# Create thread-local singleton provider for some object (main thread):
thread_local_object = providers.ThreadLocalSingleton(object)

# Create singleton provider for thread-safe queue:
queue_factory = providers.ThreadSafeSingleton(queue.Queue)

# Create callable provider for example(), inject dependencies:
example = providers.DelegatedCallable(
    example,
    example_object=thread_local_object,
    queue_object=queue_factory,
)

# Create factory for threads that are targeted to execute example():
thread_factory = providers.Factory(threading.Thread, target=example)

if __name__ == '__main__':
    # Create 10 threads for concurrent execution of example():
    threads = []
    for thread_number in range(10):
        threads.append(
            thread_factory(name='Thread{0}'.format(thread_number)),
        )

    # Start execution of all created threads:
    for thread in threads:
        thread.start()

    # Wait while threads would complete their work:
    for thread in threads:
        thread.join()

    # Making some asserts (main thread):
    all_objects = set()

    while not queue_factory().empty():
        all_objects.add(queue_factory().get())

    assert len(all_objects) == len(threads)
    # Queue contains same number of objects as number of threads where
    # thread-local singleton provider was used.
