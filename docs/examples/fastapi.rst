.. _fastapi-example:

FastAPI example
===============

.. meta::
   :keywords: Python,Dependency Injection,FastAPI,Example
   :description: This example demonstrates a usage of the FastAPI and Dependency Injector.


This example shows how to use ``Dependency Injector`` with `FastAPI <https://fastapi.tiangolo.com/>`_.

The example application is a REST API that searches for funny GIFs on the `Giphy <https://giphy.com/>`_.

The source code is available on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/fastapi>`_.

Application structure
---------------------

Application has next structure:

.. code-block:: bash

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── endpoints.py
   │   ├── giphy.py
   │   ├── services.py
   │   └── tests.py
   ├── config.yml
   └── requirements.txt

Container
---------

Declarative container is defined in ``giphynavigator/containers.py``:

.. literalinclude:: ../../examples/miniapps/fastapi/giphynavigator/containers.py
   :language: python

Endpoints
---------

Endpoint has a dependency on search service. There are also some config options that are used as default values.
The dependencies are injected using :ref:`wiring` feature.

Listing of ``giphynavigator/endpoints.py``:

.. literalinclude:: ../../examples/miniapps/fastapi/giphynavigator/endpoints.py
   :language: python

Application factory
-------------------
Application factory creates container, wires it with the ``endpoints`` module, creates
``FastAPI`` app, and setup routes.

Listing of ``giphynavigator/application.py``:

.. literalinclude:: ../../examples/miniapps/fastapi/giphynavigator/application.py
   :language: python

Tests
-----

Tests use :ref:`provider-overriding` feature to replace giphy client with a mock ``giphynavigator/tests.py``:

.. literalinclude:: ../../examples/miniapps/fastapi/giphynavigator/tests.py
   :language: python
   :emphasize-lines: 29,57,72

Sources
-------

Explore the sources on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/fastapi>`_.

.. include:: ../sponsor.rst

.. disqus::
