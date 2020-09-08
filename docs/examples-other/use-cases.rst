Use cases example
=================

.. meta::
   :keywords: Python,Dependency Injection,Inversion of Control,Container,Example,Application,
              Framework,DependenciesContainer
   :description: This example demonstrates a usage of the DependenciesContainer provider.

This example demonstrates a usage of the ``DependenciesContainer`` provider.

The source code is available on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/decoupled-packages>`_.

Application structure
---------------------

Example application has next structure:

.. code-block:: bash


   ./
   └── example/
       ├── __init__.py
       ├── __main__.py
       ├── adapters.py
       ├── containers.py
       └── usecases.py

Containers
----------

Listing of the ``example/containers.py``:

.. literalinclude:: ../../examples/miniapps/use-cases/example/containers.py
   :language: python

Main module
-----------

Listing of the ``example/__main__.py``:

.. literalinclude:: ../../examples/miniapps/use-cases/example/__main__.py
   :language: python


Run the application
-------------------

Instructions for running in the "test" mode:

.. code-block:: bash

    python run.py test example@example.com

Instructions for running in the "prod" mode:

.. code-block:: bash

    python run.py prod example@example.com

Adapters and use cases
----------------------

Listing of the ``example/adapters.py``:

.. literalinclude:: ../../examples/miniapps/use-cases/example/adapters.py
   :language: python

Listing of the ``example/usecases.py``:

.. literalinclude:: ../../examples/miniapps/use-cases/example/usecases.py
   :language: python

.. disqus::
