.. _resource-provider:

Resource provider
=================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Resource,Injection,
              Logging,Event Loop,Thread Pool
   :description: Resource provider provides a component with initialization and shutdown. It works
                 well for configuring logging, event loop, thread or process pool, etc.
                 This page demonstrates how to use resource provider.

.. currentmodule:: dependency_injector.providers

:py:class:`Resource` provider provides a component with initialization and shutdown.

.. literalinclude:: ../../examples/providers/resource.py
   :language: python
   :lines: 3-

Resource providers help to initialize and configure logging, event loop, thread or process pool, etc.

Resource provider is similar to ``Singleton``. Resource initialization happens only once.
You can do injections and use provided instance the same way like you do with any other provider.

.. code-block:: python
   :emphasize-lines: 12

   class Container(containers.DeclarativeContainer):

       config = providers.Configuration()

       thread_pool = providers.Resource(
           init_threat_pool,
           max_workers=config.max_workers,
       )

       dispatcher = providers.Factory(
           TaskDispatcher,
           executor=thread_pool,
       )

Container has an interface to initialize and shutdown all resources:

.. code-block:: python

   container = Container()
   container.init_resources()
   container.shutdown_resources()

You also can initialize and shutdown resources using ``init()`` and ``shutdown()``
methods of the provider:

.. code-block:: python

   container = Container()
   container.thread_pool.init()
   container.thread_pool.shutdown()

Resource provider supports 3 types of resource initializers:

- Function
- Generator
- Subclass of ``resources.Resource``

Function initializer
--------------------

Function is the most common way to specify resource initialization:

.. code-block:: python

   def init_resource(argument1=..., argument2=...):
       return SomeResource()


   class Container(containers.DeclarativeContainer):

       resource = providers.Resource(
           init_resource,
           argument1=...,
           argument2=...,
       )

Function initializer should not necessarily return a value. This often happens when
you configure global resource:

.. code-block:: python

   import logging.config


   class Container(containers.DeclarativeContainer):

       configure_logging = providers.Resource(
           logging.config.fileConfig,
           fname='logging.ini',
       )

Function initializer does not support shutdown.

Generator initializer
---------------------

Resource provider can use 2-step generators:

- First step of generator is an initialization phase
- The second is step is a shutdown phase

.. code-block:: python

   def init_resource(argument1=..., argument2=...):
       resource = SomeResource()  # initialization

       yield resource

       # shutdown
       ...


   class Container(containers.DeclarativeContainer):

       resource = providers.Resource(
           init_resource,
           argument1=...,
           argument2=...,
       )

Generator initialization phase ends on the first ``yield`` statement. You can return a
resource object using ``yield resource`` like in the example above. Returning of the
object is not mandatory. You can leave ``yield`` statement empty:

.. code-block:: python

   def init_resource(argument1=..., argument2=...):
       # initialization
       ...

       yield

       # shutdown
       ...


   class Container(containers.DeclarativeContainer):

       resource = providers.Resource(
           init_resource,
           argument1=...,
           argument2=...,
       )

Subclass initializer
--------------------

You can provide resource initializer by implementing a subclass of ``resources.Resource``:

.. code-block:: python

   from dependency_injector import resources


   class MyResource(resources.Resource):

       def init(self, argument1=..., argument2=...) -> SomeResource:
           return SomeResource()

       def shutdown(self, resource: SomeResource) -> None:
           # shutdown
           ...


   class Container(containers.DeclarativeContainer):

       resource = providers.Resource(
           MyResource,
           argument1=...,
           argument2=...,
       )

Subclass must implement two methods: ``.init()`` and ``.shutdown()``.

Method ``.init()`` receives arguments specified in resource provider.
It performs initialization and returns resource object. Returning of the object
is not mandatory.

Method ``.shutdown()`` receives resource object returned from ``.init()``. If ``.init()``
didn't return an object ``.shutdown()`` method will be called anyway with ``None`` as a
first argument.

.. code-block:: python

   from dependency_injector import resources


   class MyResource(resources.Resource):

       def init(self, argument1=..., argument2=...) -> None:
           # initialization
           ...

       def shutdown(self, _: None) -> None:
           # shutdown
           ...

.. disqus::
