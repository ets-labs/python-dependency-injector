Container providers traversal
-----------------------------

To traverse container providers use method ``.traverse()``.

.. literalinclude:: ../../examples/containers/traverse.py
   :language: python
   :lines: 3-
   :emphasize-lines: 38

Method ``.traverse()`` returns a generator. Traversal generator visits all container providers.
This includes nested providers even if they are not present on the root level of the container.

Traversal generator guarantees that each container provider will be visited only once.
It can traverse cyclic provider graphs.

Traversal generator does not guarantee traversal order.

You can use ``types=[...]`` argument to filter providers. Traversal generator will only return
providers matching specified types.

.. code-block:: python
   :emphasize-lines: 3

   container = Container()

   for provider in container.traverse(types=[providers.Resource]):
       print(provider)

    # <dependency_injector.providers.Resource(<function init_database at 0x10bd2cb80>) at 0x10d346b40>
    # <dependency_injector.providers.Resource(<function init_cache at 0x10be373a0>) at 0x10d346bc0>

.. disqus::
