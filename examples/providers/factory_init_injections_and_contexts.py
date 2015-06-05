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
user1 = users_factory(1)  # Same as: User(1,
                          #               main_photo=Photo(),
                          #               credit_card=CreditCard())
user2 = users_factory(2)  # Same as: User(2,
                          #               main_photo=Photo(),
                          #               credit_card=CreditCard())

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
