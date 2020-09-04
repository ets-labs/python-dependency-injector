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

It helps implementing the dependency injection principle.

What is dependency injection?
-----------------------------

Dependency injection is a principle that helps to decrease coupling and increase cohesion.

What is coupling and cohesion?

Coupling and cohesion are about how tough the components are tied.

- **High coupling**. If the coupling is high it's like using a superglue or welding. No easy way
  to disassemble.
- **High cohesion**. High cohesion is like using the screws. Very easy to disassemble and
  assemble back or assemble a different way. It is an alternative to high coupling.

When the cohesion is high the coupling is low.

High cohesion brings the flexibility. Your code becomes easier to change and test.

How to implement dependency injection?
--------------------------------------

Objects do not create each other anymore. They provide a way to inject the dependencies instead.

Before:

.. code-block:: python

   import os


   class ApiClient:

       def __init__(self):
           self.api_key = os.getenv('API_KEY')  # <-- the dependency
           self.timeout = os.getenv('TIMEOUT')  # <-- the dependency


   class Service:

       def __init__(self):
           self.api_client = ApiClient()  # <-- the dependency


   if __name__ == '__main__':
       service = Service()


After:

.. code-block:: python

   import os


   class ApiClient:

       def __init__(self, api_key: str, timeout: int):
           self.api_key = api_key  # <-- the dependency is injected
           self.timeout = timeout  # <-- the dependency is injected


   class Service:

       def __init__(self, api_client: ApiClient):
           self.api_client = api_client  # <-- the dependency is injected


   if __name__ == '__main__':
       service = Service(ApiClient(os.getenv('API_KEY'), os.getenv('TIMEOUT')))


``ApiClient`` is decoupled from knowing where the options come from. You can read a key and a
timeout from a configuration file or even get them from a database.

``Service`` is decoupled from the ``ApiClient``. It does not create it anymore. You can provide a
stub or other compatible object.

Flexibility comes with a price.

Now you need to assemble your objects like this
``Service(ApiClient(os.getenv('API_KEY'), os.getenv('TIMEOUT')))``. The assembly code might get
duplicated and it'll become harder to change the application structure.

What does Dependency Injector do?
---------------------------------

``Dependency Injector`` helps to assemble the objects.

It provides you the container and the providers that help you describe objects assembly. When you
need an object you get it from the container. The rest of the assembly work is done by the
framework:

.. code-block:: python

   from dependency_injector import containers, providers


   class ApiClient:

       def __init__(self, api_key: str, timeout: int):
           self.api_key = api_key
           self.timeout = timeout


   class Service:

       def __init__(self, api_client: ApiClient):
           self.api_client = api_client


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration()

       api_client = providers.Singleton(
           ApiClient,
           api_key=config.api_key,
           timeout=config.timeout.as_int(),
       )

       service = providers.Factory(
           Service,
           api_client=api_client,
       )


   if __name__ == '__main__':
       container = Container()
       container.config.api_key.from_env('API_KEY')
       container.config.timeout.from_env('TIMEOUT')

       service = container.service()

Retrieving of the ``Service`` instance now is done like this ``container.service()``.

Objects assembling is consolidated in the container. When you need to make a change you do it in
one place.

When doing the testing you call the ``container.api_client.override()`` to replace the real API
client with a mock:

.. code-block:: python

   from unittest import mock


   with container.api_client.override(mock.Mock()):
       service = container.service()

It helps in a testing. Also you can use it for configuring project for the different environments:
replace an API client with a stub on the dev or stage.

`More examples <https://github.com/ets-labs/python-dependency-injector/tree/master/examples>`_

Installation
------------

The package is available on the `PyPi`_::

    pip install dependency-injector

Documentation
-------------

The documentation is available on the `Read The Docs <http://python-dependency-injector.ets-labs.org/>`_

Tutorials
---------

Choose one of the following:

- `Flask web application tutorial <http://python-dependency-injector.ets-labs.org/tutorials/flask.html>`_
- `Aiohttp REST API tutorial <http://python-dependency-injector.ets-labs.org/tutorials/aiohttp.html>`_
- `Asyncio monitoring daemon tutorial <http://python-dependency-injector.ets-labs.org/tutorials/asyncio-daemon.html>`_
- `CLI application tutorial <http://python-dependency-injector.ets-labs.org/tutorials/cli.html>`_

Concept
-------

``Dependency Injector`` stands on two principles:

- Explicit is better than implicit (PEP20).
- Do no magic to your code.

How is it different from the other frameworks?

- **No autowiring.** The framework does NOT do any autowiring / autoresolving of the dependencies. You need to specify everything explicitly. Because *"Explicit is better than implicit" (PEP20)*.
- **Does not pollute your code.** Your application does NOT know and does NOT depend on the framework. No ``@inject`` decorators, annotations, patching or any other magic tricks.

``Dependency Injector`` makes a simple contract with you:

- You tell the framework how to assemble your objects
- The framework does it for you

The power of the ``Dependency Injector`` is in its simplicity and straightforwardness. It is a simple tool for the powerful concept.

Frequently asked questions
--------------------------

What is the dependency injection?
 - dependency injection is a principle that decreases coupling and increases cohesion

Why should I do the dependency injection?
 - your code becomes more flexible, testable and clear
 - you have no problems when you need to understand how it works or change it 😎 

How do I start doing the dependency injection?
 - you start writing the code following the dependency injection principle
 - you register all of your application components and their dependencies in the container
 - when you need a component, you get it from the container

Why do I need a framework for this?
 - you need the framework for this to not create it by your own
 - this framework gives you the container and the providers
 - the container is like a dictionary with the batteries 🔋 
 - the providers manage the lifetime of your components, you will need factories, singletons, smart config object etc

What price do I pay and what do I get?
 - you need to explicitly specify the dependencies in the container
 - it will be extra work in the beginning
 - it will payoff when project grows or in two weeks 😊 (when you forget what project was about)

What features does the framework have?
 - building objects graph
 - smart configuration object
 - providers: factory, singleton, thread locals registers, etc
 - positional and keyword context injections
 - overriding of the objects in any part of the graph

What features the framework does NOT have?
 - autowiring / autoresolving of the dependencies
 - the annotations and ``@inject``-like decorators

Have a question?
 - Open a `Github Issue <https://github.com/ets-labs/python-dependency-injector/issues>`_

Found a bug?
 - Open a `Github Issue <https://github.com/ets-labs/python-dependency-injector/issues>`_

Want to help?
 - |star| Star the ``Dependency Injector`` on the `Github <https://github.com/ets-labs/python-dependency-injector/>`_
 - |new| Start a new project with the ``Dependency Injector``
 - |tell| Tell your friend about the ``Dependency Injector``

Want to contribute?
 - |fork| Fork the project
 - |pull| Open a pull request to the ``develop`` branch

.. _PyPi: https://pypi.org/project/dependency-injector/

.. |star| unicode:: U+2B50 U+FE0F .. star sign1
.. |new| unicode:: U+1F195 .. new sign
.. |tell| unicode:: U+1F4AC .. tell sign
.. |fork| unicode:: U+1F500 .. fork sign
.. |pull| unicode:: U+2B05 U+FE0F .. pull sign
