.. _providers:

Providers
=========

Providers help you to define how objects are created. They manage objects lifetime and their
dependencies.

Each provider is a callable. You call the provider like a function when you need to create an
object or call a function. Provider calls all dependent providers to retrieve the dependencies
and injects them.

Any of the providers can be overridden by another provider. When provider is overridden it calls
to the overriding provider. This helps in testing or overriding API clients with stubs for dev or
stage environment.

Providers package API docs - :py:mod:`dependency_injector.providers`

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
