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

    # Creating several User objects:
    user1 = users_factory()
    user2 = users_factory()

    # Making some asserts:
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
      injectable value right after object's creation. Takes attribute's name
      and injectable value.
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

.. image:: /images/factory_init_injections.png

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
useful for testing).

So, please, follow the example below:

.. image:: /images/factory_init_injections_and_contexts.png

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

Example:

.. image:: /images/factory_attribute_injections.png

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

Example:

.. image:: /images/factory_method_injections.png

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

