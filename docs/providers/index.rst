.. _providers:

Providers
=========

Providers help to assemble the objects. They create objects and inject the dependencies.

Each provider is a callable. You call the provider like a function when you need to create an
object. Provider retrieves the underlying dependencies and inject them into the created object.
It causes the cascade effect that helps to assemble object graphs.

.. code-block:: bash

   provider1()
   │
   ├──> provider2()
   │
   ├──> provider3()
   │    │
   │    └──> provider4()
   │
   └──> provider5()
        │
        └──> provider6()

Another providers feature is an overriding. Any of the providers can be overridden by another
provider. When provider is overridden it calls to the overriding provider instead of providing
the object by its own. This helps in testing. This also helps in overriding API clients with
stubs for the development or staging environment. See the example at :ref:`provider-overriding`.

Providers module API docs - :py:mod:`dependency_injector.providers`

..  toctree::
    :maxdepth: 2

    factory
    singleton
    callable
    coroutine
    object
    list
    configuration
    selector
    dependency
    overriding
    provided_instance
    custom
