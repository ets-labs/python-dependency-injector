.. _fastapi-sqlalchemy-example:

FastAPI + SQLAlchemy example
============================

.. meta::
   :keywords: Python,Dependency Injection,FastAPI,SQLAlchemy,Example
   :description: This example demonstrates a usage of the FastAPI, SQLAlchemy, and Dependency Injector.

This example shows how to use ``Dependency Injector`` with `FastAPI <https://fastapi.tiangolo.com/>`_ and
`SQLAlchemy <https://www.sqlalchemy.org/>`_.

The source code is available on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/fastapi-sqlalchemy>`_.

Thanks to `@ShvetsovYura <https://github.com/ShvetsovYura>`_ for providing initial example:
`FastAPI_DI_SqlAlchemy <https://github.com/ShvetsovYura/FastAPI_DI_SqlAlchemy>`_.

Application structure
---------------------

Application has next structure:

.. code-block:: bash

   ./
   ├── webapp/
   │   ├── __init__.py
   │   ├── application.py
   │   ├── containers.py
   │   ├── database.py
   │   ├── endpoints.py
   │   ├── models.py
   │   ├── repositories.py
   │   ├── services.py
   │   └── tests.py
   ├── config.yml
   ├── docker-compose.yml
   ├── Dockerfile
   └── requirements.txt

Application factory
-------------------

Application factory creates container, wires it with the ``endpoints`` module, creates
``FastAPI`` app, and setup routes.

Application factory also creates database if it does not exist.

Listing of ``webapp/application.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-sqlalchemy/webapp/application.py
   :language: python

Endpoints
---------

Module ``endpoints`` contains example endpoints. Endpoints have a dependency on user service.
User service is injected using :ref:`wiring` feature. See ``webapp/endpoints.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-sqlalchemy/webapp/endpoints.py
   :language: python

Container
---------

Declarative container wires example user service, user repository, and utility database class.
See ``webapp/containers.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-sqlalchemy/webapp/containers.py
   :language: python

Services
--------

Module ``services`` contains example user service. See ``webapp/services.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-sqlalchemy/webapp/services.py
   :language: python

Repositories
------------

Module ``repositories`` contains example user repository. See ``webapp/repositories.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-sqlalchemy/webapp/repositories.py
   :language: python

Models
------

Module ``models`` contains example SQLAlchemy user model. See ``webapp/models.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-sqlalchemy/webapp/models.py
   :language: python

Database
--------

Module ``database`` defines declarative base and utility class with engine and session factory.
See ``webapp/database.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-sqlalchemy/webapp/database.py
   :language: python

Tests
-----

Tests use :ref:`provider-overriding` feature to replace repository with a mock. See ``webapp/tests.py``:

.. literalinclude:: ../../examples/miniapps/fastapi-sqlalchemy/webapp/tests.py
   :language: python
   :emphasize-lines: 25, 45, 58, 74, 86, 97

Sources
-------

The source code is available on the `Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/fastapi-sqlalchemy>`_.

.. include:: ../sponsor.rst

.. disqus::
