Writing catalogs
----------------

Catalogs have to extend base catalog class ``di.AbstractCatalog``.

Providers have to be defined like catalog's attributes. Every provider in
catalog has name. This name should follow ``some_provider`` convention, 
that is standard naming convention for attribute names in Python.

.. note::

    It might be useful to add such ``""":type: di.Provider -> Object1"""`` 
    docstrings just on the next line after provider's definition.  It will 
    help code analyzing tools and IDE's to understand that variable above 
    contains some callable object, that returns particular instance as a 
    result of its call.

Here is an simple example of catalog with several factories:

.. image:: /images/catalogs/writing_catalogs.png
    :width: 85%
    :align: center

.. literalinclude:: ../../examples/catalogs/writing_catalogs.py
   :language: python
