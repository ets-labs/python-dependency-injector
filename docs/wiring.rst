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

Decorator @inject
-----------------

Decorator ``@inject`` injects the dependencies. Use it to decorate all functions and methods
with the injections.

.. code-block:: python

   from dependency_injector.wiring import inject, Provide


   @inject
   def foo(bar: Bar = Provide[Container.bar]):
       ...

Decorator ``@inject`` must be specified as a very first decorator of a function to ensure that
the wiring works appropriately. This will also contribute to the performance of the wiring process.

.. code-block:: python

   from dependency_injector.wiring import inject, Provide


   @decorator_etc
   @decorator_2
   @decorator_1
   @inject
   def foo(bar: Bar = Provide[Container.bar]):
       ...

Specifying the ``@inject`` as a first decorator is also crucial for FastAPI, other frameworks
using decorators similarly, for closures, and for any types of custom decorators with the injections.

FastAPI example:

.. code-block:: python

   app = FastAPI()


   @app.api_route("/")
   @inject
   async def index(service: Annotated[Service, Depends(Provide[Container.service])]):
       value = await service.process()
       return {"result": value}

Decorators example:

.. code-block:: python

   def decorator1(func):
       @functools.wraps(func)
       @inject
       def wrapper(value1: int = Provide[Container.config.value1]):
           result = func()
           return result + value1
       return wrapper


   def decorator2(func):
       @functools.wraps(func)
       @inject
       def wrapper(value2: int = Provide[Container.config.value2]):
           result = func()
           return result + value2
       return wrapper

   @decorator1
   @decorator2
   def sample():
       ...

.. seealso::
   `Issue #404 <https://github.com/ets-labs/python-dependency-injector/issues/404#issuecomment-785216978>`_
   explains ``@inject`` decorator in a few more details.

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

To inject the provider itself use ``Provide[foo.provider]``:

.. code-block:: python

   from dependency_injector.providers import Factory
   from dependency_injector.wiring import inject, Provide


   @inject
   def foo(bar_provider: Factory[Bar] = Provide[Container.bar.provider]):
       bar = bar_provider(argument="baz")
       ...

You can also use ``Provider[foo]`` for injecting the provider itself:

.. code-block:: python

   from dependency_injector.providers import Factory
   from dependency_injector.wiring import inject, Provider


   @inject
   def foo(bar_provider: Factory[Bar] = Provider[Container.bar]):
       bar = bar_provider(argument="baz")
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
   :emphasize-lines: 14-17
   :lines: 3-

String identifiers
------------------

You can use wiring with string identifiers. String identifier should match provider name in the container:

.. literalinclude:: ../examples/wiring/example_string_id.py
   :language: python
   :emphasize-lines: 15
   :lines: 3-

With string identifiers you don't need to use a container to specify an injection.

To specify an injection from a nested container use point ``.`` as a separator:

.. code-block:: python

   @inject
   def foo(service: UserService = Provide["services.user"]) -> None:
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
   def foo(value: int = Provide["config.option", as_int()]) -> None:
       ...


   @inject
   def foo(value: float = Provide["config.option", as_float()]) -> None:
       ...


   @inject
   def foo(value: Decimal = Provide["config.option", as_(Decimal)]) -> None:
       ...

   @inject
   def foo(value: str = Provide["config.option", required()]) -> None:
       ...

   @inject
   def foo(value: int = Provide["config.option", required().as_int()]) -> None:
       ...


   @inject
   def foo(value: int = Provide["config.option", invariant("config.switch")]) -> None:
       ...

   @inject
   def foo(value: int = Provide["service", provided().foo["bar"].call()]) -> None:
       ...


To inject a container use special identifier ``<container>``:

.. code-block:: python

   @inject
   def foo(container: Container = Provide["<container>"]) -> None:
       ...

Caveats
~~~~~~~

While using string identifiers you may not notice a typo in the identifier until the code is executed.
In order to aid with catching such errors early, you may pass `warn_unresolved=True` to the ``wire`` method and/or :class:`WiringConfiguration`:

.. code-block:: python
   :emphasize-lines: 4

   class Container(containers.DeclarativeContainer):
       wiring_config = containers.WiringConfiguration(
           modules=["yourapp.module"],
           warn_unresolved=True,
       )

Or:

.. code-block:: python
   :emphasize-lines: 4

   container = Container()
   container.wire(
       modules=["yourapp.module"],
       warn_unresolved=True,
   )


Making injections into modules and class attributes
---------------------------------------------------

You can use wiring to make injections into modules and class attributes. Both the classic marker
syntax and the ``Annotated`` form are supported.

Classic marker syntax:

.. code-block:: python

   service: Service = Provide[Container.service]

   class Main:
       service: Service = Provide[Container.service]

Full example of the classic marker syntax:

.. literalinclude:: ../examples/wiring/example_attribute.py
   :language: python
   :lines: 3-
   :emphasize-lines: 14,19

Annotated form (Python 3.9+):

.. code-block:: python

   from typing import Annotated

   service: Annotated[Service, Provide[Container.service]]

   class Main:
       service: Annotated[Service, Provide[Container.service]]

Full example of the annotated form:

.. literalinclude:: ../examples/wiring/example_attribute_annotated.py
   :language: python
   :lines: 3-
   :emphasize-lines: 16,21

You could also use string identifiers to avoid a dependency on a container:

.. code-block:: python
   :emphasize-lines: 1,6

   service: Service = Provide["service"]


   class Main:

       service: Service = Provide["service"]

Wiring with modules and packages
--------------------------------

To wire a container with the modules you need to call ``container.wire()`` method:

.. code-block:: python

   container.wire(
       modules=[
           "yourapp.module1",
           "yourapp.module2",
       ],
   )

Method ``container.wire()`` can resolve relative imports:

.. code-block:: python

   # In module "yourapp.main":

   container.wire(
       modules=[
           ".module1",  # Resolved to: "yourapp.module1"
           ".module2",  # Resolved to: "yourapp.module2"
       ],
   )

You can also manually specify a base package for resolving relative imports with
the ``from_package`` argument:

.. code-block:: python

   # In module "yourapp.main":

   container.wire(
       modules=[
           ".module1",  # Resolved to: "anotherapp.module1"
           ".module2",  # Resolved to: "anotherapp.module2"
       ],
       from_package="anotherapp",
   )

Argument ``modules`` can also take already imported modules:

.. code-block:: python

   from yourapp import module1, module2


   container = Container()
   container.wire(modules=[module1, module2])

You can wire container with a package. Container walks recursively over the package modules:

.. code-block:: python

   container.wire(
       packages=[
           "yourapp.package1",
           "yourapp.package2",
       ],
   )

Arguments ``modules`` and ``packages`` can be used together.

When wiring is done functions and methods with the markers are patched to provide injections when called.

.. code-block:: python

   @inject
   def foo(bar: Bar = Provide[Container.bar]):
       ...


   container = Container()
   container.wire(modules=[__name__])

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
           self.container.wire(modules=["yourapp.module1", "yourapp.module2"])
           self.addCleanup(self.container.unwire)

.. code-block:: python

   import pytest


   @pytest.fixture
   def container():
       container = Container()
       container.wire(modules=["yourapp.module1", "yourapp.module2"])
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

Wiring configuration
--------------------

You can specify wiring configuration in the container. When wiring configuration is defined,
container will call method ``.wire()`` automatically when you create an instance:

.. code-block:: python

   class Container(containers.DeclarativeContainer):

       wiring_config = containers.WiringConfiguration(
           modules=[
               "yourapp.module1",
               "yourapp.module2",
           ],
           packages=[
               "yourapp.package1",
               "yourapp.package2",
           ],
       )

       ...


   if __name__ == "__main__":
       container = Container()  # container.wire() is called automatically
       ...

You can also use relative imports. Container will resolve them corresponding
to the module of the container class:

.. code-block:: python

   # In module "yourapp.container":

   class Container(containers.DeclarativeContainer):

       wiring_config = containers.WiringConfiguration(
           modules=[
              ".module1",  # Resolved to: "yourapp.module1"
              ".module2",  # Resolved to: "yourapp.module2"
           ],
       )
   )


   # In module "yourapp.foo.bar.main":

   if __name__ == "__main__":
       container = Container()  # wire to "yourapp.module1" and "yourapp.module2"
       ...

To use wiring configuration and call method ``.wire()`` manually, set flag ``auto_wire=False``:

.. code-block:: python
   :emphasize-lines: 5

   class Container(containers.DeclarativeContainer):

       wiring_config = containers.WiringConfiguration(
           modules=["yourapp.module1"],
           auto_wire=False,
       )


   if __name__ == "__main__":
       container = Container()  # container.wire() is NOT called automatically
       container.wire()         # wire to "yourapp.module1"
       ...

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


   if __name__ == "__main__":
       container = Container()
       register_loader_containers(container)  # <--- installs import hook

       module = importlib.import_module("package.module")
       module.foo()

You can register multiple containers in the import hook. For doing this call register function
with multiple containers ``register_loader_containers(container1, container2, ...)``
or with a single container ``register_loader_containers(container)`` multiple times.

To unregister a container use ``unregister_loader_containers(container)``.
Wiring module will uninstall the import hook when unregister last container.

Few notes on performance
------------------------

``.wire()`` utilize caching to speed up the wiring process. At the end it clears the cache to avoid memory leaks.
But this may not always be desirable, when you want to keep the cache for the next wiring
(e.g. due to usage of multiple containers or during unit tests).

To keep the cache after wiring, you can set flag ``keep_cache=True`` (works with ``WiringConfiguration`` too):

.. code-block:: python

   container1.wire(
       modules=["yourapp.module1", "yourapp.module2"],
       keep_cache=True,
   )
   container2.wire(
       modules=["yourapp.module2", "yourapp.module3"],
       keep_cache=True,
   )
   ...

and then clear it manually when you need it:

.. code-block:: python

   from dependency_injector.wiring import clear_cache

   clear_cache()


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
- :ref:`boto3-example`
- :ref:`django-example`
- :ref:`flask-example`
- :ref:`flask-blueprints-example`
- :ref:`aiohttp-example`
- :ref:`sanic-example`
- :ref:`fastapi-example`
- :ref:`fastapi-redis-example`
- :ref:`fastapi-sqlalchemy-example`
- :ref:`fastdepends-example`

.. disqus::
