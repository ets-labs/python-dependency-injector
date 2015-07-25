Overriding of providers
-----------------------

Every provider could be overridden by another provider.

This gives opportunity to make system behaviour more flexible in some points.
The main feature is that while your code is using providers, it depends on 
providers, but not on the objects that providers provide. As a result of this, 
you can change providing by provider object to a different one, but still
compatible one, without chaning your previously written code.

Provider overriding functionality has such interface:

.. image:: /images/provider_override.png
    :width: 45%
    :align: center

+ ``Provider.override()`` - takes another provider that will be used instead of
  current provider. This method could be called several times. In such case,
  last passed provider would be used as overriding one.
+ ``Provider.reset_override()`` - resets all overriding providers. Provider 
  starts to behave itself like usual.
+ ``Provider.is_overridden`` - bool, ``True`` if provider is overridden.

.. note::

   Actually, initial provider forms stack from overriding providers. There is 
   some, not so common, but still usefull, functionality that could be used:

   + ``Provider.last_overriding`` - always keeps reference to last overriding 
     provider.
   + ``Provider.reset_last_overriding()`` - remove last overriding provider 
     from stack of overriding providers.

Example:

.. image:: /images/providers/overriding_simple.png
    :width: 80%
    :align: center

.. code-block:: python

    """Simple providers overriding example."""

    from objects.providers import Factory


    class User(object):

        """Example class User."""

    # Users factory:
    users_factory = Factory(User)

    # Creating several User objects:
    user1 = users_factory()
    user2 = users_factory()

    # Making some asserts:
    assert user1 is not user2
    assert isinstance(user1, User) and isinstance(user2, User)


    # Extending User:
    class SuperUser(User):

        """Example class SuperUser."""

    # Overriding users factory:
    users_factory.override(Factory(SuperUser))

    # Creating some more User objects using overridden users factory:
    user3 = users_factory()
    user4 = users_factory()

    # Making some asserts:
    assert user4 is not user3
    assert isinstance(user3, SuperUser) and isinstance(user4, SuperUser)

Example:

.. image:: /images/providers/overriding_users_model.png
    :width: 100%
    :align: center

.. code-block:: python

    """Overriding user's model example."""

    from objects.providers import Factory
    from objects.injections import KwArg


    class User(object):

        """Example class User."""

        def __init__(self, id, password):
            """Initializer."""
            self.id = id
            self.password = password
            super(User, self).__init__()


    class UserService(object):

        """Example class UserService."""

        def __init__(self, user_cls):
            """Initializer."""
            self.user_cls = user_cls
            super(UserService, self).__init__()

        def get_by_id(self, id):
            """Find user by his id and return user model."""
            return self.user_cls(id=id, password='secret' + str(id))

    # Users factory and UserService provider:
    users_service = Factory(UserService,
                            KwArg('user_cls', User))

    # Getting several users and making some asserts:
    user1 = users_service().get_by_id(1)
    user2 = users_service().get_by_id(2)

    assert isinstance(user1, User)
    assert user1.id == 1
    assert user1.password == 'secret1'

    assert isinstance(user2, User)
    assert user2.id == 2
    assert user2.password == 'secret2'

    assert user1 is not user2

    # Extending user model and user service for adding custom attributes without
    # making any changes to client's code.


    class ExtendedUser(User):

        """Example class ExtendedUser."""

        def __init__(self, id, password, first_name=None, last_name=None,
                     gender=None):
            """Initializer."""
            self.first_name = first_name
            self.last_name = last_name
            self.gender = gender
            super(ExtendedUser, self).__init__(id, password)


    class ExtendedUserService(UserService):

        """Example class ExtendedUserService."""

        def get_by_id(self, id):
            """Find user by his id and return user model."""
            user = super(ExtendedUserService, self).get_by_id(id)
            user.first_name = 'John' + str(id)
            user.last_name = 'Smith' + str(id)
            user.gender = 'male'
            return user

    # Overriding users_service provider:
    extended_users_service = Factory(ExtendedUserService,
                                     KwArg('user_cls', ExtendedUser))
    users_service.override(extended_users_service)

    # Getting few other users users and making some asserts:
    user3 = users_service().get_by_id(3)
    user4 = users_service().get_by_id(4)

    assert isinstance(user3, ExtendedUser)
    assert user3.id == 3
    assert user3.password == 'secret3'
    assert user3.first_name == 'John3'
    assert user3.last_name == 'Smith3'

    assert isinstance(user4, ExtendedUser)
    assert user4.id == 4
    assert user4.password == 'secret4'
    assert user4.first_name == 'John4'
    assert user4.last_name == 'Smith4'

    assert user3 is not user4
