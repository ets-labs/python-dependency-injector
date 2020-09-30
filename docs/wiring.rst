.. _wiring:

Wiring
======

Wiring feature provides a way to inject container providers into the functions and methods.

To use wiring you need:

- **Place markers in the code**. Wiring marker specifies what provider to inject,
  e.g. ``Provide[Container.bar]``. This helps container to find the injections.
- **Wire the container with the markers in the code**. Call ``container.wire()``
  specifying modules and packages you would like to wire it with.
- **Use functions and classes as you normally do**. Framework will provide specified injections.

.. literalinclude:: ../examples/wiring/example.py
   :language: python
   :lines: 3-

Markers
-------

Wiring feature uses markers to make injections. Injection marker is specified as a default value of
a function or method argument:

.. code-block:: python

   from dependency_injector.wiring import Provide


   def foo(bar: Bar = Provide[Container.bar]):
       ...

Specifying an annotation is optional.

There are two types of markers:

- ``Provide[foo]`` - call the provider ``foo`` and injects the result
- ``Provider[foo]`` - injects the provider ``foo`` itself

.. code-block:: python

   from dependency_injector.wiring import Provider


   def foo(bar_provider: Callable[..., Bar] = Provider[Container.bar]):
       bar = bar_provider()
       ...

You can use configuration, provided instance and sub-container providers as you normally do.

.. code-block:: python

   def foo(token: str = Provide[Container.config.api_token]):
       ...


   def foo(timeout: int = Provide[Container.config.timeout.as_(int)]):
       ...


   def foo(baz: Baz = Provide[Container.bar.provided.baz]):
       ...


   def foo(bar: Bar = Provide[Container.subcontainer.bar]):
       ...

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
   Python has a limitation on patching already imported individual members. To protect from errors
   prefer an import of modules instead of individual members or make sure that imports happen
   after the wiring:

   .. code-block:: python

      from . import module

      module.fn()

      # instead of

      from .module import fn

      fn()

Integration with other frameworks
---------------------------------

Wiring feature helps integrate the container providers with other frameworks:
Django, Flask, Aiohttp, Sanic, your custom framework, etc.

With wiring you do not need to change the traditional application structure of your framework.

1. Create a container and put framework-independent components as providers.
2. Place wiring markers in the functions and methods where you want the providers
   to be injected (Flask or Django views, Aiohttp or Sanic handlers, etc).
3. Wire the container with the application.
4. Run the application.

.. literalinclude:: ../examples/wiring/flask_example.py
   :language: python
   :lines: 3-

.. disqus::
