What is dependency injection and inversion of control?
------------------------------------------------------

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control
   :description: This article provides definition of dependency injection, 
                 inversion of control and dependency inversion. It contains 
                 example code in Python that is refactored to be following 
                 inversion of control principle and then enhanced by 
                 inversion of control container based on "Dependency Injector" 
                 declarative catalog.

Definition
~~~~~~~~~~

Wikipedia provides quite good definitions of dependency injection pattern
and related principles:

.. glossary::

    `Dependency injection`_
        In software engineering, dependency injection is a software design 
        pattern that implements inversion of control for resolving 
        dependencies. A dependency is an object that can be used (a service). 
        An injection is the passing of a dependency to a dependent object (a 
        client) that would use it. The service is made part of the client's 
        state. Passing the service to the client, rather than allowing a 
        client to build or find the service, is the fundamental requirement of 
        the pattern.

        Dependency injection allows a program design to follow the dependency 
        inversion principle. The client delegates to external code (the 
        injector) the responsibility of providing its dependencies. The client 
        is not allowed to call the injector code. It is the injecting code 
        that constructs the services and calls the client to inject them. This 
        means the client code does not need to know about the injecting code. 
        The client does not need to know how to construct the services. The 
        client does not need to know which actual services it is using. The 
        client only needs to know about the intrinsic interfaces of the 
        services because these define how the client may use the services. 
        This separates the responsibilities of use and construction.

    `Inversion of control`_
        In software engineering, inversion of control (IoC) describes a design 
        in which custom-written portions of a computer program receive the 
        flow of control from a generic, reusable library. A software 
        architecture with this design inverts control as compared to 
        traditional procedural programming: in traditional programming, the 
        custom code that expresses the purpose of the program calls into 
        reusable libraries to take care of generic tasks, but with inversion 
        of control, it is the reusable code that calls into the custom, or 
        task-specific, code.

        Inversion of control is used to increase modularity of the program and 
        make it extensible, and has applications in object-oriented 
        programming and other programming paradigms. The term was popularized 
        by Robert C. Martin and Martin Fowler.

        The term is related to, but different from, the dependency inversion 
        principle, which concerns itself with decoupling dependencies between 
        high-level and low-level layers through shared abstractions.

    `Dependency inversion`_
        In object-oriented programming, the dependency inversion principle 
        refers to a specific form of decoupling software modules. When 
        following this principle, the conventional dependency relationships 
        established from high-level, policy-setting modules to low-level, 
        dependency modules are reversed, thus rendering high-level modules 
        independent of the low-level module implementation details. The 
        principle states:

            + High-level modules should not depend on low-level modules. 
              Both should depend on abstractions.
            + Abstractions should not depend on details. 
              Details should depend on abstractions.

        The principle inverts the way some people may think about 
        object-oriented design, dictating that both high- and low-level 
        objects must depend on the same abstraction. 

Example
~~~~~~~

Let's go through the code of ``example.py``:

.. literalinclude:: ../../examples/ioc_di_demos/example.py
   :language: python
   :linenos:

At some point, things defined above mean, that the code from ``example.py``, 
could look different, like in ``ioc_example.py``:

.. literalinclude:: ../../examples/ioc_di_demos/ioc_example.py
   :language: python
   :linenos:

Also the code from ``ioc_example.py`` could be upgraded with inversion of 
control container, like in ``ioc_container_example.py``:

.. literalinclude:: ../../examples/ioc_di_demos/ioc_container_example.py
   :language: python
   :linenos:
    
.. note::

    ``Components`` from ``ioc_container_example.py`` is an IoC container. It 
    contains a collection of component providers that could be injected into 
    each other. 

    Assuming this, ``Components`` could be one and the only place, where 
    application's structure is being managed on the high level.

Best explanation, ever
~~~~~~~~~~~~~~~~~~~~~~

Some times ago `user198313`_ posted awesome `question`_ about dependency 
injection on `StackOverflow`_:

.. note:: 

    How to explain dependency injection to a 5-year-old?

And `John Munsch`_ provided absolutely Great answer:

.. note:: 

    When you go and get things out of the refrigerator for yourself, you can 
    cause problems. You might leave the door open, you might get something 
    Mommy or Daddy doesn't want you to have. You might even be looking for 
    something we don't even have or which has expired.

    What you should be doing is stating a need, "I need something to drink 
    with lunch," and then we will make sure you have something when you sit 
    down to eat.


.. _Dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
.. _Inversion of control: https://en.wikipedia.org/wiki/Inversion_of_control
.. _Dependency inversion: https://en.wikipedia.org/wiki/Dependency_inversion_principle
.. _StackOverflow: http://stackoverflow.com/
.. _question: http://stackoverflow.com/questions/1638919/how-to-explain-dependency-injection-to-a-5-year-old/1639186
.. _user198313: http://stackoverflow.com/users/198313/user198313
.. _John Munsch: http://stackoverflow.com/users/31899/john-munsch
