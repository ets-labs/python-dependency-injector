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

``Flask`` + ``Dependency Injector`` example application container:

.. code-block:: python

    from dependency_injector import containers, providers
    from dependency_injector.ext import flask
    from flask import Flask
    from github import Github

    from . import views, services


    class ApplicationContainer(containers.DeclarativeContainer):
        """Application container."""

        app = flask.Application(Flask, __name__)

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

        index_view = flask.View(
            views.index,
            search_service=search_service,
            default_search_term=config.search.default_term,
            default_search_limit=config.search.default_limit,
        )

Running such container looks like this:

.. code-block:: python

    from .containers import ApplicationContainer


    def create_app():
        """Create and return Flask application."""
        container = ApplicationContainer()
        container.config.from_yaml('config.yml')
        container.config.github.auth_token.from_env('GITHUB_TOKEN')

        app = container.app()
        app.container = container

        app.add_url_rule('/', view_func=container.index_view.as_view())

        return app

And testing looks like:

.. code-block:: python

    from unittest import mock

    import pytest
    from github import Github
    from flask import url_for

    from .application import create_app


    @pytest.fixture
    def app():
        return create_app()


    def test_index(client, app):
        github_client_mock = mock.Mock(spec=Github)
        # Configure mock

        with app.container.github_client.override(github_client_mock):
            response = client.get(url_for('index'))

        assert response.status_code == 200
        # Do more asserts

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

- |star| Star the ``Dependency Injector`` on the `Github <https://github.com/ets-labs/python-dependency-injector/>`_
- |new| Start a new project with the ``Dependency Injector``
- |tell| Tell your friend about the ``Dependency Injector``

Want to contribute?
-------------------

- |fork| Fork the project
- |pull| Open a pull request to the ``develop`` branch

.. _PyPi: https://pypi.org/project/dependency-injector/

.. |star| unicode:: U+2B50 U+FE0F .. star sign1
.. |new| unicode:: U+1F195 .. new sign
.. |tell| unicode:: U+1F4AC .. tell sign
.. |fork| unicode:: U+1F500 .. fork sign
.. |pull| unicode:: U+2B05 U+FE0F .. pull sign
