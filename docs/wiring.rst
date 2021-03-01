.. _wiring:

Wiring
======

Wiring feature provides a way to inject container providers into the functions and methods.

To use wiring you need:

- **Place @inject decorator**. Decorator ``@inject`` injects the dependencies.
- **Place markers**. Wiring marker specifies what dependency to inject,
  e.g. ``Provide[Container.bar]``. This helps container to find the injections.
- **Wire the container with the markers in the code**. Call ``container.wire()``
  specifying modules and packages you would like to wire it with.
- **Use functions and classes as you normally do**. Framework will provide specified injections.

.. literalinclude:: ../examples/wiring/example.py
   :language: python
   :lines: 3-

.. contents::
   :local:
   :backlinks: none

Markers
-------

Wiring feature uses markers to make injections. Injection marker is specified as a default value of
a function or method argument:

.. code-block:: python

   from dependency_injector.wiring import inject, Provide


   @inject
   def foo(bar: Bar = Provide[Container.bar]):
       ...

Specifying an annotation is optional.

There are two types of markers:

- ``Provide[foo]`` - call the provider ``foo`` and injects the result
- ``Provider[foo]`` - injects the provider ``foo`` itself

.. code-block:: python

   from dependency_injector.wiring import inject, Provider


   @inject
   def foo(bar_provider: Callable[..., Bar] = Provider[Container.bar]):
       bar = bar_provider()
       ...

You can use configuration, provided instance and sub-container providers as you normally do.

.. code-block:: python

   @inject
   def foo(token: str = Provide[Container.config.api_token]):
       ...


   @inject
   def foo(timeout: int = Provide[Container.config.timeout.as_(int)]):
       ...


   @inject
   def foo(baz: Baz = Provide[Container.bar.provided.baz]):
       ...


   @inject
   def foo(bar: Bar = Provide[Container.subcontainer.bar]):
       ...


You can compound wiring and ``Resource`` provider to implement per-function execution scope.
See :ref:`Resources, wiring and per-function execution scope <resource-provider-wiring-closing>` for details.

Also you can use ``Provide`` marker to inject a container.

.. literalinclude:: ../examples/wiring/example_container.py
   :language: python
   :emphasize-lines: 16-19
   :lines: 3-

Strings identifiers
-------------------

You can use wiring with string identifiers. String identifier should match provider name in the container:

.. literalinclude:: ../examples/wiring/example_string_id.py
   :language: python
   :emphasize-lines: 17
   :lines: 3-

With string identifiers you don't need to use a container to specify an injection.

To specify an injection from a nested container use point ``.`` as a separator:

.. code-block:: python

   @inject
   def foo(service: UserService = Provide['services.user']) -> None:
       ...

You can also use injection modifiers:

.. code-block:: python

   from dependency_injector.wiring import (
       inject,
       Provide,
       as_int,
       as_float,
       as_,
       required,
       invariant,
       provided,
   )


   @inject
   def foo(value: int = Provide['config.option', as_int()]) -> None:
       ...


   @inject
   def foo(value: float = Provide['config.option', as_float()]) -> None:
       ...


   @inject
   def foo(value: Decimal = Provide['config.option', as_(Decimal)]) -> None:
       ...

   @inject
   def foo(value: str = Provide['config.option', required()]) -> None:
       ...

   @inject
   def foo(value: int = Provide['config.option', required().as_int()]) -> None:
       ...


   @inject
   def foo(value: int = Provide['config.option', invariant('config.switch')]) -> None:
       ...

   @inject
   def foo(value: int = Provide['service', provided().foo['bar'].call()]) -> None:
       ...


To inject a container use special identifier ``<container>``:

.. code-block:: python

   @inject
   def foo(container: Container = Provide['<container>']) -> None:
       ...


Making injections into modules and class attributes
---------------------------------------------------

You can use wiring to make injections into modules and class attributes.

.. literalinclude:: ../examples/wiring/example_attribute.py
   :language: python
   :lines: 3-
   :emphasize-lines: 16,21

You could also use string identifiers to avoid a dependency on a container:

.. code-block:: python
   :emphasize-lines: 1,6

   service: Service = Provide['service']


   class Main:

       service: Service = Provide['service']

Wiring with modules and packages
--------------------------------

To wire a container with a module you need to call ``container.wire(modules=[...])`` method. Argument
``modules`` is an iterable of the module objects.

.. code-block:: python

   from yourapp import module1, module2


   container = Container()
   container.wire(modules=[module1, module2])

You can wire container with a package. Container walks recursively over package modules.

.. code-block:: python

   from yourapp import package1, package2


   container = Container()
   container.wire(packages=[package1, package2])

Arguments ``modules`` and ``packages`` can be used together.

When wiring is done functions and methods with the markers are patched to provide injections when called.

.. code-block:: python

   @inject
   def foo(bar: Bar = Provide[Container.bar]):
       ...


   container = Container()
   container.wire(modules=[sys.modules[__name__]])

   foo()  # <--- Argument "bar" is injected

Injections are done as keyword arguments.

.. code-block:: python

   foo()  # Equivalent to:
   foo(bar=container.bar())

Context keyword arguments have a priority over injections.

.. code-block:: python

   foo(bar=Bar())  # Bar() is injected

To unpatch previously patched functions and methods call ``container.unwire()`` method.

.. code-block:: python

   container.unwire()

You can use that in testing to re-create and re-wire a container before each test.

.. code-block:: python

   import unittest


   class SomeTest(unittest.TestCase):

       def setUp(self):
           self.container = Container()
           self.container.wire(modules=[module1, module2])
           self.addCleanup(self.container.unwire)

.. code-block:: python

   import pytest


   @pytest.fixture
   def container():
       container = Container()
       container.wire(modules=[module1, module2])
       yield container
       container.unwire()

.. note::
   Wiring can take time if you have a large codebase. Consider to persist a container instance and
   avoid re-wiring between tests.

.. note::
   Python has a limitation on patching individually imported functions. To protect from errors
   prefer importing modules to importing individual functions or make sure imports happen
   after the wiring:

   .. code-block:: python

      # Potential error:

      from .module import fn

      fn()

   Instead use next:

   .. code-block:: python

      # Always works:

      from . import module

      module.fn()

.. _async-injections-wiring:

Asynchronous injections
-----------------------

Wiring feature supports asynchronous injections:

.. code-block:: python

   class Container(containers.DeclarativeContainer):

       db = providers.Resource(init_async_db_client)

       cache = providers.Resource(init_async_cache_client)


   @inject
   async def main(
       db: Database = Provide[Container.db],
       cache: Cache = Provide[Container.cache],
   ):
       ...

When you call asynchronous function wiring prepares injections asynchronously.
Here is what it does for previous example:

.. code-block:: python

    db, cache = await asyncio.gather(
        container.db(),
        container.cache(),
    )

    await main(db=db, cache=cache)

You can also use ``Closing`` marker with the asynchronous ``Resource`` providers:

.. code-block:: python

   @inject
   async def main(
       db: Database = Closing[Provide[Container.db]],
       cache: Cache = Closing[Provide[Container.cache]],
   ):
       ...

Wiring does closing asynchronously:

.. code-block:: python

    db, cache = await asyncio.gather(
        container.db(),
        container.cache(),
    )

    await main(db=db, cache=cache)

    await asyncio.gather(
        container.db.shutdown(),
        container.cache.shutdown(),
    )

See :ref:`Resources, wiring and per-function execution scope <resource-provider-wiring-closing>` for
details on ``Closing`` marker.

.. note::

   Wiring does not not convert asynchronous injections to synchronous.

   It handles asynchronous injections only for ``async def`` functions. Asynchronous injections into
   synchronous ``def`` function still work, but you need to take care of awaitables by your own.

See also:

- Provider :ref:`async-injections`
- Resource provider :ref:`resource-async-initializers`
- :ref:`fastapi-redis-example`

Wiring of dynamically imported modules
--------------------------------------

You can install an import hook that automatically wires containers to the imported modules.
This is useful when you import modules dynamically.

.. code-block:: python

   import importlib

   from dependency_injector.wiring import register_loader_containers

   from .containers import Container


   if __name__ == '__main__':
       container = Container()
       register_loader_containers(container)  # <--- installs import hook

       module = importlib.import_module('package.module')
       module.foo()

You can register multiple containers in the import hook. For doing this call register function
with multiple containers ``register_loader_containers(container1, container2, ...)``
or with a single container ``register_loader_containers(container)`` multiple times.

To unregister a container use ``unregister_loader_containers(container)``.
Wiring module will uninstall the import hook when unregister last container.

Integration with other frameworks
---------------------------------

Wiring feature helps to integrate with other frameworks like Django, Flask, etc.

With wiring you do not need to change the traditional application structure of your framework.

1. Create a container and put framework-independent components as providers.
2. Place wiring markers in the functions and methods where you want the providers
   to be injected (Flask or Django views, Aiohttp or Sanic handlers, etc).
3. Wire the container with the application modules.
4. Run the application.

.. literalinclude:: ../examples/wiring/flask_example.py
   :language: python
   :lines: 3-

Take a look at other application examples:

- :ref:`application-single-container`
- :ref:`application-multiple-containers`
- :ref:`decoupled-packages`
- :ref:`boto3`
- :ref:`django-example`
- :ref:`flask-example`
- :ref:`flask-blueprints-example`
- :ref:`aiohttp-example`
- :ref:`sanic-example`
- :ref:`fastapi-example`
- :ref:`fastapi-redis-example`
- :ref:`fastapi-sqlalchemy-example`

.. disqus::
