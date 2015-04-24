Providers
=========

Providers are strategies of accessing objects.

All providers are callable. They describe how particular objects will be
provided.


Instance providers & Injections
-------------------------------

*Instance* providers are providers that deal with object's creation and
initialization.

There are few *Instance* providers:

    - ``NewInstance`` provider creates new instance of specified class on every
      call.
    - ``Singleton`` provider creates new instance of specified class on first
      call and returns same instance on every next call.

Example:

.. code-block:: python

    """`NewInstance` and `Singleton` providers example."""

    from objects.providers import NewInstance
    from objects.providers import Singleton


    # NewInstance provider creates new instance of specified class on every call.
    new_object = NewInstance(object)

    object_1 = new_object()
    object_2 = new_object()

    assert object_1 is not object_2
    assert isinstance(object_1, object) and isinstance(object_2, object)

    # Singleton provider creates new instance of specified class on first call
    # and returns same instance on every next call.
    single_object = Singleton(object)

    single_object_1 = single_object()
    single_object_2 = single_object()

    assert single_object_1 is single_object_2
    assert isinstance(object_1, object) and isinstance(object_2, object)


Objects can take dependencies in various forms. Some objects take init
arguments, other are using attributes or methods to be initialized. It affects
how such objects need to be created and initialized, and that is the place
where *Injections* need to be used.

In terms of computer science, *Injection* of dependency is a way how
dependency can be coupled with dependent object.

In terms of *Objects*, *Injection* is an instruction how to provide
dependency for the particular object.

Every Python object could be an injection's value. Special case is an *Objects*
provider as an injection's value. In such case, injection value is a result of
injectable provider call (every time injection is done).

There are several types of injections. Below is a description of how they are
used by instance providers:

    - ``KwArg`` - is injected in object's ``__init__()`` method in time of
      object's initialization via keyword argument.
    - ``Attribute`` - is injected into object's attribute (not class attribute)
      after object's initialization.
    - ``Method`` - is injected into object method's call after objects
      initialization.

Example:

.. code-block:: python

    """`NewInstance` and `Singleton` providers with injections example."""

    import sqlite3

    from objects.providers import Singleton
    from objects.providers import NewInstance

    from objects.injections import KwArg
    from objects.injections import Attribute


    class ObjectA(object):

        """ObjectA has dependency on database."""

        def __init__(self, database):
            """Initializer.

            Database dependency need to be injected via init arg."""
            self.database = database

        def get_one(self):
            """Select one from database and return it."""
            return self.database.execute('SELECT 1').fetchone()[0]


    # Database and `ObjectA` providers.
    database = Singleton(sqlite3.Connection,
                         KwArg('database', ':memory:'),
                         KwArg('timeout', 30),
                         KwArg('detect_types', True),
                         KwArg('isolation_level', 'EXCLUSIVE'),
                         Attribute('row_factory', sqlite3.Row))

    object_a = NewInstance(ObjectA,
                           KwArg('database', database))

    # Creating several `ObjectA` instances.
    object_a_1 = object_a()
    object_a_2 = object_a()

    # Making some asserts.
    assert object_a_1 is not object_a_2
    assert object_a_1.database is object_a_2.database is database()
    assert object_a_1.get_one() == object_a_2.get_one() == 1

Static providers
----------------

Static providers are family of providers that return their values "as is".
There are four of static providers: ``Class``, ``Object``, ``Function`` and
``Value``. All of them has the same behaviour, but usage of anyone is
predicted by readability and providable object's type.

Example:

.. code-block:: python

    """Static providers example."""

    from objects.providers import Class
    from objects.providers import Object
    from objects.providers import Function
    from objects.providers import Value


    cls_provider = Class(object)
    assert cls_provider() is object

    object_provider = Object(object())
    assert isinstance(object_provider(), object)

    function_provider = Function(len)
    assert function_provider() is len

    value_provider = Value(123)
    assert value_provider() == 123

Callable providers
------------------

``Callable`` provider is a provider that decorates particular callable with
some injections. Every call of this provider returns result of call of initial
callable.

Example:

 .. code-block:: python

    """`Callable` providers examples."""

    from objects.providers import Callable
    from objects.providers import Singleton

    from objects.injections import KwArg

    import sqlite3


    def some_function(arg, database):
        """Example function that has input arg and dependency on database."""
        return database.execute('SELECT @1', [arg]).fetchone()[0]


    # Database and `ObjectA` providers.
    database = Singleton(sqlite3.Connection,
                         KwArg('database', ':memory:'))

    some_function = Callable(some_function,
                             KwArg('database', database))

    # Some asserts.
    assert some_function(1) == 1
    assert some_function(2) == 2
    assert some_function(2231) == 2231


External dependency providers
-----------------------------

``ExternalDependency`` provider can be useful for development of
self-sufficient libraries / modules / applications, that has required external
dependencies.

For example, you have created self-sufficient library / module / application,
that has dependency on *database connection*.

Second step you want to do is to make this software component to be easy
reusable by wide amount of developers and to be easily integrated into many
applications.

It may be good idea, to move all external dependencies (like
*dabase connection*)  to the top level and make them to be injected on your
software component's initialization. It will make third party developers feel
themselves free about integration of yours component in their applications,
because of they would be able to find right place / right way for doing this
in their application's architectures.

On the other side,
you can be sure, that your external dependency will be satisfied by appropriate
instance.

Example:

.. code-block:: python

    """External dependency providers example."""

    import sqlite3

    from objects.providers import Singleton
    from objects.providers import NewInstance
    from objects.providers import ExternalDependency

    from objects.injections import KwArg
    from objects.injections import Attribute


    class ObjectA(object):

        """ObjectA has dependency on database."""

        def __init__(self, database):
            """Initializer.

            Database dependency need to be injected via init arg."""
            self.database = database

        def get_one(self):
            """Select one from database and return it."""
            return self.database.execute('SELECT 1').fetchone()[0]


    # Database and `ObjectA` providers.
    database = ExternalDependency(instance_of=sqlite3.Connection)

    object_a = NewInstance(ObjectA,
                           KwArg('database', database))

    # Satisfaction of external dependency.
    database.override(Singleton(sqlite3.Connection,
                                KwArg('database', ':memory:'),
                                KwArg('timeout', 30),
                                KwArg('detect_types', True),
                                KwArg('isolation_level', 'EXCLUSIVE'),
                                Attribute('row_factory', sqlite3.Row)))

    # Creating several `ObjectA` instances.
    object_a_1 = object_a()
    object_a_2 = object_a()

    # Making some asserts.
    assert object_a_1 is not object_a_2
    assert object_a_1.database is object_a_2.database is database()


Config providers
----------------

Providers delegation
--------------------

Overriding of providers
-----------------------

Any provider can be overridden by another provider.

Example:

.. code-block:: python

    """Providers overriding example."""

    import sqlite3

    from objects.providers import Singleton
    from objects.providers import NewInstance

    from objects.injections import KwArg
    from objects.injections import Attribute


    class ObjectA(object):

        """ObjectA has dependency on database."""

        def __init__(self, database):
            """Initializer.

            Database dependency need to be injected via init arg."""
            self.database = database

        def get_one(self):
            """Select one from database and return it."""
            return self.database.execute('SELECT 1')


    class ObjectAMock(ObjectA):

        """Mock of ObjectA.

        Has no dependency on database.
        """

        def __init__(self):
            """Initializer."""

        def get_one(self):
            """Select one from database and return it.

            Mock makes no database queries and always returns two instead of one.
            """
            return 2


    # Database and `ObjectA` providers.
    database = Singleton(sqlite3.Connection,
                         KwArg('database', ':memory:'),
                         KwArg('timeout', 30),
                         KwArg('detect_types', True),
                         KwArg('isolation_level', 'EXCLUSIVE'),
                         Attribute('row_factory', sqlite3.Row))

    object_a = NewInstance(ObjectA,
                           KwArg('database', database))


    # Overriding `ObjectA` provider with `ObjectAMock` provider.
    object_a.override(NewInstance(ObjectAMock))

    # Creating several `ObjectA` instances.
    object_a_1 = object_a()
    object_a_2 = object_a()

    # Making some asserts.
    assert object_a_1 is not object_a_2
    assert object_a_1.get_one() == object_a_2.get_one() == 2
