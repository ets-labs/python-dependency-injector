.. _aiohttp-example:

Aiohttp example
===============

.. meta::
   :keywords: Python,Dependency Injection,Aiohttp,Example
   :description: This example demonstrates a usage of the Aiohttp and Dependency Injector.


This example shows how to use ``Dependency Injector`` with `Aiohttp <https://docs.aiohttp.org/>`_.

The example application is a REST API that searches for funny GIFs on the `Giphy <https://giphy.com/>`_.

The source code is available on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/aiohttp>`_.

:ref:`aiohttp-tutorial` demonstrates how to build this application step-by-step.

Application structure
---------------------

Application has next structure:

.. code-block:: bash

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── giphy.py
   │   ├── handlers.py
   │   ├── services.py
   │   └── tests.py
   ├── config.yml
   └── requirements.txt

Container
---------

Declarative container is defined in ``giphynavigator/containers.py``:

.. literalinclude:: ../../examples/miniapps/aiohttp/giphynavigator/containers.py
   :language: python

Handlers
--------

Handler has dependencies on search service and some config options. The dependencies are injected
using :ref:`wiring` feature.

Listing of ``giphynavigator/handlers.py``:

.. literalinclude:: ../../examples/miniapps/aiohttp/giphynavigator/handlers.py
   :language: python

Application factory
-------------------
Application factory creates container, wires it with the ``handlers`` module, creates
``Aiohttp`` app and setup routes.

Listing of ``giphynavigator/application.py``:

.. literalinclude:: ../../examples/miniapps/aiohttp/giphynavigator/application.py
   :language: python

Tests
-----

Tests use :ref:`provider-overriding` feature to replace giphy client with a mock ``giphynavigator/tests.py``:

.. literalinclude:: ../../examples/miniapps/aiohttp/giphynavigator/tests.py
   :language: python
   :emphasize-lines: 32,59,73

Sources
-------

Explore the sources on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/aiohttp>`_.

.. include:: ../sponsor.rst

.. disqus::
