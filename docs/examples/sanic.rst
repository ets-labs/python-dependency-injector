.. _sanic-example:

Sanic example
==============

.. meta::
   :keywords: Python,Dependency Injection,Sanic,Example
   :description: This example demonstrates a usage of the Sanic and Dependency Injector.


This example shows how to use ``Dependency Injector`` with `Sanic <https://sanic.readthedocs.io/en/latest/>`_.

The example application is a REST API that searches for funny GIFs on the `Giphy <https://giphy.com/>`_.

The source code is available on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/sanic>`_.

Application structure
---------------------

Application has next structure:

.. code-block:: bash

   ./
   ├── giphynavigator/
   │   ├── __init__.py
   │   ├── __main__.py
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

.. literalinclude:: ../../examples/miniapps/sanic/giphynavigator/containers.py
   :language: python

Handlers
--------

Handler has dependencies on search service and some config options. The dependencies are injected
using :ref:`wiring` feature.

Listing of ``giphynavigator/handlers.py``:

.. literalinclude:: ../../examples/miniapps/sanic/giphynavigator/handlers.py
   :language: python

Application factory
-------------------
Application factory creates container, wires it with the ``handlers`` module, creates
``Sanic`` app and setup routes.

Listing of ``giphynavigator/application.py``:

.. literalinclude:: ../../examples/miniapps/sanic/giphynavigator/application.py
   :language: python

Tests
-----

Tests use :ref:`provider-overriding` feature to replace giphy client with a mock ``giphynavigator/tests.py``:

.. literalinclude:: ../../examples/miniapps/sanic/giphynavigator/tests.py
   :language: python
   :emphasize-lines: 34,61,75

Sources
-------

Explore the sources on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/sanic>`_.

.. include:: ../sponsor.rst

.. disqus::
