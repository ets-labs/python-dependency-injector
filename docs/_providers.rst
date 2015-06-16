Providers
=========


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
*database connection*)  to the top level and make them to be injected on your
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
    from objects.providers import Factory
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

    object_a_factory = Factory(ObjectA,
                               KwArg('database', database))

    # Satisfaction of external dependency.
    database.override(Singleton(sqlite3.Connection,
                                KwArg('database', ':memory:'),
                                KwArg('timeout', 30),
                                KwArg('detect_types', True),
                                KwArg('isolation_level', 'EXCLUSIVE'),
                                Attribute('row_factory', sqlite3.Row)))

    # Creating several `ObjectA` instances.
    object_a_1 = object_a_factory()
    object_a_2 = object_a_factory()

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

    from objects.providers import Factory
    from objects.providers import Singleton

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

    object_a_factory = Factory(ObjectA,
                               KwArg('database', database))


    # Overriding `ObjectA` provider with `ObjectAMock` provider.
    object_a_factory.override(Factory(ObjectAMock))

    # Creating several `ObjectA` instances.
    object_a_1 = object_a_factory()
    object_a_2 = object_a_factory()

    # Making some asserts.
    assert object_a_1 is not object_a_2
    assert object_a_1.get_one() == object_a_2.get_one() == 2




.. _Constructor injection: http://en.wikipedia.org/wiki/Dependency_injection#Constructor_injection
