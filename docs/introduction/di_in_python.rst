Dependency injection and inversion of control in Python
-------------------------------------------------------

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control
   :description: This article describes benefits of dependency injection and
                 inversion of control for Python applications. Also it
                 contains some Python examples that show how dependency
                 injection and inversion could be implemented. In addition, it
                 demonstrates usage of dependency injection framework,
                 IoC container and such popular design pattern as Factory.

History
~~~~~~~

Originally, dependency injection pattern got popular in languages with static
typing, like Java. Dependency injection framework can
significantly improve flexibility of the language with static typing. Also,
implementation of dependency injection framework for language with static
typing is not something that one can do shortly, it could be quite complex
thing to be done well.

While Python is very flexible interpreted language with dynamic typing, there
is a meaning that dependency injection doesn't work for it as well, as it does
for Java. Also there is a meaning that dependency injection framework is
something that Python developer would not ever need, cause dependency injection
could be implemented easily using language fundamentals.

Discussion
~~~~~~~~~~

It is true.

Partly.

Dependency injection, as a software design pattern, has number of
advantages that are common for each language (including Python):

+ Dependency Injection decreases coupling between a class and its dependency.
+ Because dependency injection doesn't require any change in code behavior it
  can be applied to legacy code as a refactoring. The result is clients that
  are more independent and that are easier to unit test in isolation using
  stubs or mock objects that simulate other objects not under test. This ease
  of testing is often the first benefit noticed when using dependency
  injection.
+ Dependency injection can be used to externalize a system's configuration
  details into configuration files allowing the system to be reconfigured
  without recompilation (rebuilding). Separate configurations can be written
  for different situations that require different implementations of
  components. This includes, but is not limited to, testing.
+ Reduction of boilerplate code in the application objects since all work to
  initialize or set up dependencies is handled by a provider component.
+ Dependency injection allows a client to remove all knowledge of a concrete
  implementation that it needs to use. This helps isolate the client from the
  impact of design changes and defects. It promotes reusability, testability
  and maintainability.
+ Dependency injection allows a client the flexibility of being configurable.
  Only the client's behavior is fixed. The client may act on anything that
  supports the intrinsic interface the client expects.

.. note::

    While improved testability is one the first benefits of using dependency
    injection, it could be easily overwhelmed by monkey-patching technique,
    that works absolutely great in Python (you can monkey-patch anything,
    anytime).  At the same time, monkey-patching has nothing similar with
    other advantages defined above. Also monkey-patching technique is
    something that could be considered like too dirty to be used in production.

The complexity of dependency injection pattern implementation in Python is
definitely quite lower than in other languages (even with dynamic typing).

.. note::

    Low complexity of dependency injection pattern implementation in Python
    still means that some code should be written, reviewed, tested and
    supported.

Talking about inversion of control, it is a software design principle that
also works for each programming language, not depending on its typing type.

Inversion of control is used to increase modularity of the program and make
it extensible.

Main design purposes of using inversion of control are:

+ To decouple the execution of a task from implementation.
+ To focus a module on the task it is designed for.
+ To free modules from assumptions about how other systems do what they do and
  instead rely on contracts.
+ To prevent side effects when replacing a module.

Example
~~~~~~~

Let's go through next example:

.. image:: /images/miniapps/engines_cars/diagram.png
    :width: 100%
    :align: center

Listing of ``example.engines`` module:

.. literalinclude:: ../../examples/miniapps/engines_cars/example/engines.py
   :language: python

Listing of ``example.cars`` module:

.. literalinclude:: ../../examples/miniapps/engines_cars/example/cars.py
   :language: python

Next example demonstrates creation of several cars with different engines:

.. literalinclude:: ../../examples/miniapps/engines_cars/example_di.py
   :language: python

While previous example demonstrates advantages of dependency injection, there
is a disadvantage demonstration as well - creation of car requires additional
code for specification of dependencies. Nevertheless, this disadvantage could
be easily avoided by using a dependency injection framework for creation of
inversion of control container (IoC container).

Example of creation of several inversion of control containers (IoC containers)
using :doc:`Dependency Injector <../index>`:

.. literalinclude:: ../../examples/miniapps/engines_cars/example_ioc_containers.py
   :language: python

What's next?
~~~~~~~~~~~~

Choose one of the following as a next step:

- Look at application examples:
    - :ref:`application-single-container`
    - :ref:`application-multiple-containers`
    - :ref:`decoupled-packages`
- Pass the tutorials:
    - :ref:`flask-tutorial`
    - :ref:`aiohttp-tutorial`
    - :ref:`asyncio-daemon-tutorial`
    - :ref:`cli-tutorial`
- Know more about the :ref:`providers`
- Go to the :ref:`contents`

Useful links
~~~~~~~~~~~~

There are some useful links related to dependency injection design pattern
that could be used for further reading:

+ https://en.wikipedia.org/wiki/Dependency_injection
+ https://martinfowler.com/articles/injection.html
+ https://github.com/ets-labs/python-dependency-injector
+ https://pypi.org/project/dependency-injector/

.. disqus::
