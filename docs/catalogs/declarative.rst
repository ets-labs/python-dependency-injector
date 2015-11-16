Declarative catalogs
--------------------

.. module:: dependency_injector.catalogs

:py:class:`DeclarativeCatalog` is a catalog of providers that could be 
defined in declarative manner. It should cover most of the cases when 
list of providers that would be included in catalog is deterministic 
(catalog will not change its structure in runtime).

Declarative catalogs have to extend base declarative catalog class - 
:py:class:`dependency_injector.catalogs.DeclarativeCatalog`.

Declarative catalog's providers have to be defined like catalog's class 
attributes. Every provider in catalog has name. This name should follow 
``some_provider`` convention, that is standard naming convention for 
attribute names in Python.

.. note::

    Declarative catalogs have several features that could be useful 
    for some kind of operations on catalog's providers, please visit API 
    documentation for getting full list of features - 
    :py:class:`dependency_injector.catalogs.DeclarativeCatalog`.

.. note::

    It might be useful to add such 
    ``""":type: dependency_injector.providers.Provider -> Object1"""`` 
    docstrings just on the next line after provider's definition.  It will 
    help code analyzing tools and IDE's to understand that variable above 
    contains some callable object, that returns particular instance as a 
    result of its call.

Here is an simple example of declarative catalog with several factories:

.. image:: /images/catalogs/declarative.png
    :width: 85%
    :align: center

.. literalinclude:: ../../examples/catalogs/declarative.py
   :language: python

Example of declarative catalogs inheritance:

.. image:: /images/catalogs/declarative_inheritance.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/catalogs/declarative_inheritance.py
   :language: python

Example of declarative catalog's provider injections:

.. image:: /images/catalogs/declarative_injections.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/catalogs/declarative_injections.py
   :language: python
