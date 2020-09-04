What is dependency injection?
-----------------------------

.. meta::
   :keywords: Python,DI,Dependency injection,Low coupling,High cohesion
   :description: This page provides a Python example of what is dependency injection. It tells
                 about benefits of coupling and high cohesion.

Dependency injection is a principle that helps to decrease coupling and increase cohesion.

.. image:: images/coupling-cohesion.png

What is coupling and cohesion?

Coupling and cohesion are about how tough the components are tied.

- **High coupling**. If the coupling is high it's like using a superglue or welding. No easy way
  to disassemble.
- **High cohesion**. High cohesion is like using the screws. Very easy to disassemble and
  assemble back or assemble a different way. It is an alternative to high coupling.

When the cohesion is high the coupling is low.

High cohesion brings the flexibility. Your code becomes easier to change and to test.

The example
~~~~~~~~~~~

How does dependency injection helps to achieve high cohesion?

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

Here comes the ``Dependency Injector``.

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

How to explain dependency injection to a 5-year-old?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some time ago `user198313`_ posted this `question`_ on the `StackOverflow`_.

`John Munsch`_ provided a great answer:

    *When you go and get things out of the refrigerator for yourself, you can
    cause problems. You might leave the door open, you might get something 
    Mommy or Daddy doesn't want you to have. You might even be looking for 
    something we don't even have or which has expired.*

    *What you should be doing is stating a need, "I need something to drink
    with lunch," and then we will make sure you have something when you sit 
    down to eat.*

What's next?
~~~~~~~~~~~~

Choose one of the following as a next step:

+ Pass one of the tutorials:
    + :ref:`cli-tutorial`
    + :ref:`flask-tutorial`
    + :ref:`aiohttp-tutorial`
    + :ref:`asyncio-daemon-tutorial`
+ Know more about the :ref:`providers`
+ Go to the :ref:`contents`

.. disqus::

.. _StackOverflow: http://stackoverflow.com/
.. _question: http://stackoverflow.com/questions/1638919/how-to-explain-dependency-injection-to-a-5-year-old/1639186
.. _user198313: http://stackoverflow.com/users/198313/user198313
.. _John Munsch: http://stackoverflow.com/users/31899/john-munsch
