Catalogs
========

Catalogs are collections of providers. Main purpose of catalogs is to group
providers. 

There are, actually, several popular cases of catalogs usage:

- Grouping of providers from the same architectural layer (for example, 
  ``Services``, ``Models`` and ``Forms`` catalogs).
- Grouping of providers from the same functional groups (for example,
  catalog ``Users``, that contains all functional parts of ``Users``
  component).

Also, for both of these and some other cases, it might be useful to attach 
some init / shutdown functionality or something else, that deals with group 
of providers.

..  toctree::
    :maxdepth: 2

    declarative
    dynamic
    bundles
    overriding
