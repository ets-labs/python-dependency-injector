.. _singleton-provider:

Singleton provider
==================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Singleton,Pattern,Example,
              Threads,Multithreading,Scoped
   :description: Singleton provider helps to provide a single object. This page
                 demonstrates how to use a Singleton provider. It also provides the example
                 of using a singleton and thread locals singleton in the multi-threaded
                 environment.

.. currentmodule:: dependency_injector.providers

:py:class:`Singleton` provider provides single object. It memorizes the first created object and
returns it on the rest of the calls.

.. literalinclude:: ../../examples/providers/singleton.py
   :language: python
   :lines: 3-

``Singleton`` provider handles dependencies injection the same way like a :ref:`factory-provider`.

.. note::

   ``Singleton`` provider makes dependencies injection only when it creates an object. When an object
   is created and memorized ``Singleton`` provider just returns it without applying injections.

Specialization of the provided type and abstract singletons work the same like like for the
factories:

- :ref:`factory-specialize-provided-type`
- :ref:`abstract-factory`

``Singleton`` provider scope is tied to the container. Two different containers will provider
two different singleton objects:

.. literalinclude:: ../../examples/providers/singleton_multiple_containers.py
   :language: python
   :lines: 3-

Resetting memorized object
--------------------------

To reset a memorized object you need to call the ``.reset()`` method of the ``Singleton``
provider.

.. literalinclude:: ../../examples/providers/singleton_resetting.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18

.. note::
   Resetting of the memorized object clears the reference to it. Further object's lifecycle is
   managed by the garbage collector.

You can use ``.reset()`` method with a context manager. Memorized instance will be reset on
both entering and exiting a context.

.. literalinclude:: ../../examples/providers/singleton_resetting_with.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18-19

Context manager ``.reset()`` returns resetting singleton provider. You can use it for aliasing.

.. code-block:: python

   with container.user_service.reset() as user_service:
       ...

Method ``.reset()`` resets only current provider. To reset all dependent singleton providers
call ``.full_reset()`` method.

.. literalinclude:: ../../examples/providers/singleton_full_resetting.py
   :language: python
   :lines: 3-
   :emphasize-lines: 25

Method ``.full_reset()`` supports context manager interface like ``.reset()`` does.

.. code-block:: python

   with container.user_service.full_reset() as user_service:
       ...

See also: :ref:`reset-container-singletons`.

Using singleton with multiple threads
-------------------------------------

``Singleton`` provider is NOT thread-safe. You need to explicitly establish a synchronization for
using the ``Singleton`` provider in the multi-threading application. Otherwise you could trap
into the race condition problem: ``Singleton`` will create multiple objects.

There are two thread-safe singleton implementations out of the box:

+ :py:class:`ThreadSafeSingleton` - is a thread-safe version of a ``Singleton`` provider. You can use
  in multi-threading applications without additional synchronization.
+ :py:class:`ThreadLocalSingleton` - is a singleton provider that uses thread-locals as a storage.
  This type of singleton will manage multiple objects - the one object for the one thread.

.. literalinclude:: ../../examples/providers/singleton_thread_locals.py
   :language: python
   :lines: 3-
   :emphasize-lines: 13,15

Implementing scopes
-------------------

To implement a scoped singleton provider use a ``Singleton`` provider and reset its scope when
needed.

.. literalinclude:: ../../examples/providers/singleton_scoped.py
   :language: python
   :lines: 3-

The output should look like this (each request a ``Service`` object has a different address):

.. code-block:: bash

    * Serving Flask app "singleton_scoped" (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   <__main__.Service object at 0x1099a9d90>
   127.0.0.1 - - [25/Aug/2020 17:33:11] "GET / HTTP/1.1" 200 -
   <__main__.Service object at 0x1099a9cd0>
   127.0.0.1 - - [25/Aug/2020 17:33:17] "GET / HTTP/1.1" 200 -
   <__main__.Service object at 0x1099a9d00>
   127.0.0.1 - - [25/Aug/2020 17:33:18] "GET / HTTP/1.1" 200 -
   <__main__.Service object at 0x1099a9e50>
   127.0.0.1 - - [25/Aug/2020 17:33:18] "GET / HTTP/1.1" 200 -
   <__main__.Service object at 0x1099a9d90>
   127.0.0.1 - - [25/Aug/2020 17:33:18] "GET / HTTP/1.1" 200 -

.. disqus::
