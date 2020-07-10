.. figure:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/logo.svg
   :target: https://github.com/ets-labs/python-dependency-injector

| 

.. image:: https://img.shields.io/pypi/v/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Latest Version
   
.. image:: https://img.shields.io/pypi/l/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: License

.. image:: https://img.shields.io/pypi/pyversions/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Supported Python versions
   
.. image:: https://img.shields.io/pypi/implementation/dependency_injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Supported Python implementations

.. image:: https://pepy.tech/badge/dependency-injector
   :target: https://pepy.tech/project/dependency-injector
   :alt: Downloads

.. image:: https://pepy.tech/badge/dependency-injector/month
   :target: https://pepy.tech/project/dependency-injector
   :alt: Downloads

.. image:: https://pepy.tech/badge/dependency-injector/week
   :target: https://pepy.tech/project/dependency-injector
   :alt: Downloads

.. image:: https://img.shields.io/pypi/wheel/dependency-injector.svg
   :target: https://pypi.org/project/dependency-injector/
   :alt: Wheel

.. image:: https://travis-ci.org/ets-labs/python-dependency-injector.svg?branch=master
   :target: https://travis-ci.org/ets-labs/python-dependency-injector
   :alt: Build Status
   
.. image:: http://readthedocs.org/projects/python-dependency-injector/badge/?version=latest
   :target: http://python-dependency-injector.ets-labs.org/
   :alt: Docs Status
   
.. image:: https://coveralls.io/repos/github/ets-labs/python-dependency-injector/badge.svg?branch=master
   :target: https://coveralls.io/github/ets-labs/python-dependency-injector?branch=master
   :alt: Coverage Status

What is ``Dependency Injector``?
================================

``Dependency Injector`` is a dependency injection framework for Python.

Why do I need it?
=================

``Dependency Injector`` helps you improve application structure.

With the ``Dependency Injector`` you keep **application structure in one place**.
This place is called **the container**. You use the container to manage all the components of the application. All the component dependencies are defined explicitly. This provides the control on the application structure. It is **easy to understand and change** it.

.. figure:: https://raw.githubusercontent.com/wiki/ets-labs/python-dependency-injector/img/di-map.svg
   :target: https://github.com/ets-labs/python-dependency-injector

*The container is like a map of your application. You always know what depends on what.*

``Flask`` + ``Dependency Injector`` example:

.. code-block:: python

    from dependency_injector import containers, providers
    from dependency_injector.ext import flask
    from github import Github

    from . import services, views


    class Application(containers.DeclarativeContainer):
        """Application container."""

        config = providers.Configuration()

        github_client = providers.Factory(
            Github,
            login_or_token=config.github.auth_token,
            timeout=config.github.request_timeout,
        )

        search_service = providers.Factory(
            services.SearchService,
            github_client=github_client,
        )

        index_view = providers.Callable(
            views.index,
            search_service=search_service,
            default_search_term=config.search.default_term,
            default_search_limit=config.search.default_limit,
        )

        app = providers.Factory(
            flask.create_app,
            name=__name__,
            routes=[
                flask.Route('/', view_provider=index_view),
            ],
        )


See complete example here - `Flask + Dependency Injector Example <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/ghnav-flask>`_

How to install?
---------------

- The package is available on the `PyPi`_::

    pip install dependency-injector

Where is the docs?
------------------

- The documentation is available on the `Read The Docs <http://python-dependency-injector.ets-labs.org/>`_

Have a question?
----------------

- Open a `Github Issue <https://github.com/ets-labs/python-dependency-injector/issues>`_

Found a bug?
------------

- Open a `Github Issue <https://github.com/ets-labs/python-dependency-injector/issues>`_

Want to help?
-------------

- ⭐️ Star the ``Dependency Injector`` on the `Github <https://github.com/ets-labs/python-dependency-injector/>`_
- 🆕 Start a new project with the ``Dependency Injector``
- 💬 Tell your friend about the ``Dependency Injector``


Want to contribute?
-------------------

- 🔀 Fork the project
- ⬅️ Open a pull request to the ``develop`` branch

.. _PyPi: https://pypi.org/project/dependency-injector/
