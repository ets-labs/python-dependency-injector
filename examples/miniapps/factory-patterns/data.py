"""Sample classes and objects."""


class SqlAlchemyDatabaseService:

    def __init__(self, session, base_class):
        self.session = session
        self.base_class = base_class


class TokensService:

    def __init__(self, id_generator, database):
        self.id_generator = id_generator
        self.database = database


class Token:
    ...


class UsersService:

    def __init__(self, id_generator, database):
        self.id_generator = id_generator
        self.database = database


class User:
    ...


# Sample objects
session = object()
id_generator = object()
