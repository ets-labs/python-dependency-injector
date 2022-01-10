.. _providers:

Providers
=========

Providers help to assemble the objects. They create objects and inject the dependencies.

Each provider is a callable. You call the provider like a function when you need to create an
object. Provider retrieves the underlying dependencies and inject them into the created object.
It causes the cascade effect that helps to assemble object graphs. See ``Factory``, ``Singleton``,
``Callable`` and other provider docs below.

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

Another providers feature is an overriding. You can override any provider with another provider.
This helps in testing. This also helps in overriding API clients with stubs for the development
or staging environment. See the example at :ref:`provider-overriding`.

If you need to inject not the whole object but the parts see :ref:`provided-instance`.

To create a new provider see :ref:`create-provider`.

Providers module API docs - :py:mod:`dependency_injector.providers`

..  toctree::
    :maxdepth: 2

    factory
    singleton
    callable
    coroutine
    object
    list
    dict
    configuration
    resource
    aggregate
    selector
    dependency
    overriding
    provided_instance
    inject_self
    custom
    async
    typing_mypy
