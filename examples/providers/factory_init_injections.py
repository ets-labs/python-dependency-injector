"""`Factory` providers with init injections example."""

from objects.providers import Factory
from objects.injections import KwArg


class User(object):

    """Example class User.

    Class User has dependencies on class Photo and class CreditCard objects,
    that have to be provided as init arguments.
    """

    def __init__(self, main_photo, credit_card):
        """Initializer.

        :param main_photo: Photo
        :param credit_card: CreditCard
        :return:
        """
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
user1 = users_factory()  # Same as: User(main_photo=Photo(),
                         #               credit_card=CreditCard())
user2 = users_factory()  # Same as: User(main_photo=Photo(),
                         #               credit_card=CreditCard())

# Making some asserts:
assert user1 is not user2
assert user1.main_photo is not user2.main_photo
assert user1.credit_card is not user2.credit_card
