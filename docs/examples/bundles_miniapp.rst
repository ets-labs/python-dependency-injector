Bundles mini application example
--------------------------------

.. currentmodule:: dependency_injector.containers

"Bundles" is an example mini application that is intented to demonstrate the 
power of dependency injection for creation of re-usable application components
("bundles") with 100% transparency of their dependencies.

Example application
~~~~~~~~~~~~~~~~~~~

"Bundles" mini application has next structure:

.. code-block:: bash

    bundles/
        bundles/               <-- Bundles package
            photos/            <-- Photos bundle
                __init__.py    <-- Photos bundle dependency injection container
                entities.py
                repositories.py
            users/             <-- Users bundle
                __init__.py    <-- Users bundle dependency injection container
                entities.py
                repositories.py
        run.py                 <-- Entrypoint


IoC containers
~~~~~~~~~~~~~~

Next two listings show :py:class:`DeclarativeContainer`'s for "users" and 
"photos" bundles.

Listing of ``bundeles/users/__init__.py``:

.. literalinclude:: ../../examples/miniapps/bundles/bundles/users/__init__.py
   :language: python
   :linenos:

.. note::

    - ``Users`` container has dependency on database.

Listing of ``bundeles/photos/__init__.py``:

.. literalinclude:: ../../examples/miniapps/bundles/bundles/photos/__init__.py
   :language: python
   :linenos:

.. note::

    - ``Photos`` container has dependencies on database and file storage.

Run application
~~~~~~~~~~~~~~~

Finally, both "bundles" are initialized by providing needed dependencies.
Initialization of dependencies happens right in the runtime, not earlier.
Generally, it means, that any part of any bundle could be overridden on the
fly.

Listing of ``run.py``:

.. literalinclude:: ../../examples/miniapps/bundles/run.py
   :language: python
   :linenos:

Links
~~~~~

+ `Dependency Injector <https://github.com/ets-labs/python-dependency-injector/>`_
+ `Full example sources <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/bundles>`_


.. disqus::
