"""`Chained Factories` pattern."""

from dependency_injector import providers

from data import (
    id_generator,
    session,
    SqlAlchemyDatabaseService,
    TokensService,
    Token,
    UsersService,
    User,
)


# "Chained Factories" pattern

database = providers.Factory(SqlAlchemyDatabaseService, session=session)

tokens = providers.Factory(
    TokensService,
    id_generator=id_generator,
    database=providers.Factory(database, base_class=Token),
)

users = providers.Factory(
    UsersService,
    id_generator=id_generator,
    database=providers.Factory(database, base_class=User),
)

tokens_service = tokens()
assert tokens_service.database.base_class is Token

users_service = users()
assert users_service.database.base_class is User

# Explanation & some more examples

# 1. Keyword arguments of upper level factory are added to lower level factory
chained_dict_factory = providers.Factory(
    providers.Factory(dict, arg1=1),
    arg2=2,
)
print(chained_dict_factory())  # prints: {'arg1': 1, 'arg2': 2}

# 2. Keyword arguments of upper level factory have priority
chained_dict_factory = providers.Factory(
    providers.Factory(dict, arg1=1),
    arg1=2,
)
print(chained_dict_factory())  # prints: {'arg1': 2}

# 3. Keyword arguments provided from context have most priority
chained_dict_factory = providers.Factory(
    providers.Factory(dict, arg1=1),
    arg1=2,
)
print(chained_dict_factory(arg1=3))  # prints: {'arg1': 3}
