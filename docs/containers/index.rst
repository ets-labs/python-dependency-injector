IoC Containers
==============

Containers are collections of providers. Main purpose of containers is to group
providers. 

There are, actually, several popular cases of containers usage:

+ Keeping all providers in a single container.
+ Grouping of providers from the same architectural layer (for example, 
  ``Services``, ``Models`` and ``Forms`` containers).
+ Grouping of providers from the same functional groups (for example,
  container ``Users``, that contains all functional parts of ``Users``
  component).

Also, for both of these and some other cases, it might be useful to attach 
some init / shutdown functionality or something else, that deals with group 
of providers.

Containers module API docs - :py:mod:`dependency_injector.containers`.

..  toctree::
    :maxdepth: 2

    declarative
    dynamic
    specialization
    overriding
