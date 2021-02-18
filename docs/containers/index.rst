.. _containers:

Containers
==========

Containers are collections of the providers.

There are several use cases how you can use containers:

+ Keeping all the providers in a single container (most common).
+ Grouping of the providers from the same architectural layer (for example,
  ``Services``, ``Models`` and ``Forms`` containers).
+ Grouping of providers from the same functional groups (for example,
  container ``Users``, that contains all functional parts of the ``users``
  package).

Containers module API docs - :py:mod:`dependency_injector.containers`.

..  toctree::
    :maxdepth: 2

    declarative
    dynamic
    specialization
    overriding
    copying
    reset_singletons
    check_dependencies
    traversal
