"""`Factory` providers with attribute injections example."""

from dependency_injector import providers
from dependency_injector import injections


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
credit_cards_factory = providers.Factory(CreditCard)
photos_factory = providers.Factory(Photo)
users_factory = providers.Factory(User,
                                  injections.Attribute('main_photo',
                                                       photos_factory),
                                  injections.Attribute('credit_card',
                                                       credit_cards_factory))

# Creating several User objects:
user1 = users_factory()
# Same as: user1 = User()
#          user1.main_photo = Photo()
#          user1.credit_card = CreditCard()
user2 = users_factory()
# Same as: user2 = User()
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
