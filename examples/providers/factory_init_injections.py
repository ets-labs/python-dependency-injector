"""`Factory` providers init injections example."""

import collections
import dependency_injector.providers as providers


CreditCard = collections.namedtuple('CreditCard', [])
Photo = collections.namedtuple('Photo', [])
User = collections.namedtuple('User', ['uid', 'main_photo', 'credit_card'])

# User, Photo and CreditCard factories:
credit_cards_factory = providers.Factory(CreditCard)
photos_factory = providers.Factory(Photo)
users_factory = providers.Factory(User,
                                  main_photo=photos_factory,
                                  credit_card=credit_cards_factory)

# Creating several User objects:
user1 = users_factory(1)
# Same as: user1 = User(1,
#                       main_photo=Photo(),
#                       credit_card=CreditCard())
user2 = users_factory(2)
# Same as: user2 = User(2,
#                       main_photo=Photo(),
#                       credit_card=CreditCard())


# Context keyword arguments have priority on keyword argument injections:
main_photo = Photo()
credit_card = CreditCard()

user3 = users_factory(3,
                      main_photo=main_photo,
                      credit_card=credit_card)
# Same as: user3 = User(3,
#                       main_photo=main_photo,
#                       credit_card=credit_card)
