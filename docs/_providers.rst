Providers
=========

Providers are strategies of accessing objects.

All providers are callable. They describe how particular objects are provided.


Factory providers
-----------------

``Factory`` provider creates new instance of specified class on every call.

Nothing could be better than brief example:

.. code-block:: python

    """`Factory` providers example."""

    from objects.providers import Factory


    class User(object):

        """Example class User."""


    # Factory provider creates new instance of specified class on every call.
    users_factory = Factory(User)

    user1 = users_factory()
    user2 = users_factory()

    assert user1 is not user2
    assert isinstance(user1, User) and isinstance(user2, User)


Factory providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Objects can take dependencies in different forms. Some objects take init
arguments, other are using attributes setting or method calls to be
initialized. It affects how such objects need to be created and initialized,
and that is the place where ``objects.injections`` need to be used.

``Factory`` provider takes various number of positional arguments, that define
what kind of dependency injections need to be done.

All of those instructions are defined in ``objects.injections`` module and are
subclasses of ``objects.injections.Injection``. There  are several types of
injections that are used by ``Factory`` provider:

    - ``KwArg`` - injection is done by passing injectable value in object's
      ``__init__()`` method in time of object's creation via keyword argument.
      Takes keyword name of ``__init__()`` argument and injectable value.
    - ``Attribute`` - injection is done by setting specified attribute with
      injectable value right after object's creation. Takes attribute name and
      injectable value.
    - ``Method`` - injection is done by calling of specified method with
      injectable value right after object's creation and attribute injections
      are done. Takes method name and injectable value.

All ``Injection``'s injectable values are provided *"as is"*, except of
providers. Providers will be called every time, when injection needs to be
done.


Factory providers and __init__ injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example below shows how to create ``Factory`` of particular class with
``__init__`` keyword argument injections which injectable values are also
provided by another factories:

.. image:: ../images/factory_init_injections.png

.. code-block:: python

    """`Factory` providers with init injections example."""

    from objects.providers import Factory
    from objects.injections import KwArg


    class User(object):

        """Example class User."""

        def __init__(self, main_photo):
            """Initializer.

            :param main_photo: Photo
            :return:
            """
            self.main_photo = main_photo
            super(User, self).__init__()


    class Photo(object):

        """Example class Photo."""


    # User and Photo factories:
    photos_factory = Factory(Photo)
    users_factory = Factory(User,
                            KwArg('main_photo', photos_factory))

    # Creating several User objects:
    user1 = users_factory()  # Same as: user1 = User(main_photo=Photo())
    user2 = users_factory()  # Same as: user2 = User(main_photo=Photo())

    # Making some asserts:
    assert isinstance(user1, User)
    assert isinstance(user1.main_photo, Photo)

    assert isinstance(user2, User)
    assert isinstance(user2.main_photo, Photo)

    assert user1 is not user2
    assert user1.main_photo is not user2.main_photo


Next example shows how ``Factory`` provider deals with positional and keyword
``__init__`` context arguments. In few words, ``Factory`` provider fully
passes positional context arguments to class's ``__init__`` method, but
keyword context arguments have priority on ``KwArg`` injections (this could be
useful for testing). So, please, follow the example below:

.. image:: ../images/factory_init_injections_and_contexts.png

.. code-block:: python

    """`Factory` providers with init injections and context arguments example."""

    from objects.providers import Factory
    from objects.injections import KwArg


    class User(object):

        """Example class User.

        Class User has to be provided with user id.

        Also Class User has dependencies on class Photo and class CreditCard
        objects.

        All of the dependencies have to be provided like __init__ arguments.
        """

        def __init__(self, id, main_photo, credit_card):
            """Initializer.

            :param id: int
            :param main_photo: Photo
            :param credit_card: CreditCard
            :return:
            """
            self.id = id
            self.main_photo = main_photo
            self.credit_card = credit_card
            super(User, self).__init__()


    class Photo(object):

        """Example class Photo."""


    class CreditCard(object):

        """Example class CreditCard."""


    # User, Photo and CreditCard factories:
    credit_cards_factory = Factory(CreditCard)
    photos_factory = Factory(Photo)
    users_factory = Factory(User,
                            KwArg('main_photo', photos_factory),
                            KwArg('credit_card', credit_cards_factory))

    # Creating several User objects:
    user1 = users_factory(1)  # Same as: user1 = User(1,
                              #                       main_photo=Photo(),
                              #                       credit_card=CreditCard())
    user2 = users_factory(2)  # Same as: user2 = User(2,
                              #                       main_photo=Photo(),
                              #                       credit_card=CreditCard())

    # Making some asserts:
    assert user1.id == 1
    assert isinstance(user1.main_photo, Photo)
    assert isinstance(user1.credit_card, CreditCard)

    assert user2.id == 2
    assert isinstance(user2.main_photo, Photo)
    assert isinstance(user2.credit_card, CreditCard)

    assert user1.main_photo is not user2.main_photo
    assert user1.credit_card is not user2.credit_card

    # Context keyword arguments have priority on KwArg injections priority:
    main_photo_mock = Photo()
    credit_card_mock = CreditCard()

    user3 = users_factory(3, main_photo=main_photo_mock,
                          credit_card=credit_card_mock)

    assert user3.id == 3
    assert user3.main_photo is main_photo_mock
    assert user3.credit_card is credit_card_mock


Factory providers and attribute injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example below shows how to create ``Factory`` of particular class with
attribute injections. Those injections are done by setting specified attributes
with injectable values right after object's creation.

.. image:: ../images/factory_attribute_injections.png

.. code-block:: python

    """`Factory` providers with attribute injections example."""

    from objects.providers import Factory
    from objects.injections import Attribute


    class User(object):

        """Example class User."""

        def __init__(self):
            """Initializer."""
            self.main_photo = None
            self.credit_card = None


    class Photo(object):

        """Example class Photo."""


    class CreditCard(object):

        """Example class CreditCard."""


    # User, Photo and CreditCard factories:
    credit_cards_factory = Factory(CreditCard)
    photos_factory = Factory(Photo)
    users_factory = Factory(User,
                            Attribute('main_photo', photos_factory),
                            Attribute('credit_card', credit_cards_factory))

    # Creating several User objects:
    user1 = users_factory()  # Same as: user1 = User()
                             #          user1.main_photo = Photo()
                             #          user1.credit_card = CreditCard()
    user2 = users_factory()  # Same as: user2 = User()
                             #          user2.main_photo = Photo()
                             #          user2.credit_card = CreditCard()

    # Making some asserts:
    assert user1 is not user2

    assert isinstance(user1.main_photo, Photo)
    assert isinstance(user1.credit_card, CreditCard)

    assert isinstance(user2.main_photo, Photo)
    assert isinstance(user2.credit_card, CreditCard)

    assert user1.main_photo is not user2.main_photo
    assert user1.credit_card is not user2.credit_card


Factory providers and method injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Current example shows how to create ``Factory`` of particular class with
method injections. Those injections are done by calling of specified method
with injectable value right after object's creation and attribute injections
are done.

Method injections are not very popular in Python due Python best practices
(usage of public attributes instead of setter methods), but it may appear in
some cases.

.. image:: ../images/factory_method_injections.png

.. code-block:: python

    """`Factory` providers with method injections example."""

    from objects.providers import Factory
    from objects.injections import Method


    class User(object):

        """Example class User."""

        def __init__(self):
            """Initializer."""
            self.main_photo = None
            self.credit_card = None

        def set_main_photo(self, photo):
            """Set user's main photo."""
            self.main_photo = photo

        def set_credit_card(self, credit_card):
            """Set user's credit card."""
            self.credit_card = credit_card


    class Photo(object):

        """Example class Photo."""


    class CreditCard(object):

        """Example class CreditCard."""


    # User, Photo and CreditCard factories:
    credit_cards_factory = Factory(CreditCard)
    photos_factory = Factory(Photo)
    users_factory = Factory(User,
                            Method('set_main_photo', photos_factory),
                            Method('set_credit_card', credit_cards_factory))

    # Creating several User objects:
    user1 = users_factory()  # Same as: user1 = User()
                             #          user1.set_main_photo(Photo())
                             #          user1.set_credit_card(CreditCard())
    user2 = users_factory()  # Same as: user2 = User()
                             #          user2.set_main_photo(Photo())
                             #          user2.set_credit_card(CreditCard())

    # Making some asserts:
    assert user1 is not user2

    assert isinstance(user1.main_photo, Photo)
    assert isinstance(user1.credit_card, CreditCard)

    assert isinstance(user2.main_photo, Photo)
    assert isinstance(user2.credit_card, CreditCard)

    assert user1.main_photo is not user2.main_photo
    assert user1.credit_card is not user2.credit_card


Singleton providers
-------------------

``Singleton`` provider creates new instance of specified class on first call
and returns same instance on every next call.

Instance providers & Injections
-------------------------------

Providers
~~~~~~~~~

*Instance* providers are providers that deal with object's creation and
initialization.

There are few *Instance* providers:

    - ``Factory`` provider creates new instance of specified class on every
      call.
    - ``Singleton`` provider creates new instance of specified class on first
      call and returns same instance on every next call.

Example:

.. code-block:: python

    """`Factory` and `Singleton` providers example."""

    from objects.providers import Factory
    from objects.providers import Singleton


    # Factory provider creates new instance of specified class on every call.
    object_factory = Factory(object)

    object_1 = object_factory()
    object_2 = object_factory()

    assert object_1 is not object_2
    assert isinstance(object_1, object) and isinstance(object_2, object)

    # Singleton provider creates new instance of specified class on first call
    # and returns same instance on every next call.
    single_object = Singleton(object)

    single_object_1 = single_object()
    single_object_2 = single_object()

    assert single_object_1 is single_object_2
    assert isinstance(object_1, object) and isinstance(object_2, object)



Injections
~~~~~~~~~~

Objects can take dependencies in various forms. Some objects take init
arguments, other are using attributes or methods to be initialized. It affects
how such objects need to be created and initialized, and that is the place
where *Injections* need to be used.

In terms of computer science, *Injection of dependency* is a way how
dependency can be coupled with dependent object.

In terms of *Objects*, *Injection* is an instruction how to provide
dependency for the particular provider.

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

    """`Factory` and `Singleton` providers with injections example."""

    import sqlite3

    from objects.providers import Singleton
    from objects.providers import Factory

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

    object_a_factory = Factory(ObjectA,
                               KwArg('database', database))

    # Creating several `ObjectA` instances.
    object_a_1 = object_a_factory()
    object_a_2 = object_a_factory()

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
