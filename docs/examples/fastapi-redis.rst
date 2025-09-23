.. _fastapi-redis-example:

FastAPI + Redis example
=======================

.. meta::
   :keywords: Python,Dependency Injection,FastAPI,Redis,Example
   :description: This example demonstrates a usage of the FastAPI, Redis, and Dependency Injector.

This example shows how to use ``Dependency Injector`` with `FastAPI <https://fastapi.tiangolo.com/>`_ and
`Redis <https://redis.io/>`_.

The source code is available on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/fastapi-redis>`_.

See also:

- Provider :ref:`async-injections`
- Resource provider :ref:`resource-async-initializers`
- Wiring :ref:`async-injections-wiring`

Application structure
---------------------

Application has next structure:

.. code-block:: bash

   ./
   ├── fastapiredis/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── redis.py
   │   ├── services.py
   │   └── tests.py
   ├── docker-compose.yml
   ├── Dockerfile
   └── requirements.txt

Redis
-----

Module ``redis`` defines Redis connection pool initialization and shutdown. See ``fastapiredis/redis.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-redis/fastapiredis/redis.py
   :language: python

Service
-------

Module ``services`` contains example service. Service has a dependency on Redis connection pool.
It uses it for getting and setting a key asynchronously. Real life service will do something more meaningful.
See ``fastapiredis/services.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-redis/fastapiredis/services.py
   :language: python

Container
---------

Declarative container wires example service with Redis connection pool. See ``fastapiredis/containers.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-redis/fastapiredis/containers.py
   :language: python

Application
-----------

Module ``application`` creates ``FastAPI`` app, setup endpoint, and init container.

Endpoint ``index`` has a dependency on example service. The dependency is injected using :ref:`wiring` feature.

Listing of ``fastapiredis/application.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-redis/fastapiredis/application.py
   :language: python

Tests
-----

Tests use :ref:`provider-overriding` feature to replace example service with a mock. See ``fastapiredis/tests.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-redis/fastapiredis/tests.py
   :language: python
   :emphasize-lines: 24

Sources
-------

The source code is available on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/fastapi-redis>`_.

See also:

- Provider :ref:`async-injections`
- Resource provider :ref:`resource-async-initializers`
- Wiring :ref:`async-injections-wiring`

.. include:: ../sponsor.rst

.. disqus::
