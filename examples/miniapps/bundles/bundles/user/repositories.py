"""User repositories module."""


class UserRepository:

    def __init__(self, entity_factory, db):
        self.entity_factory = entity_factory
        self.db = db

    def get(self, id):
        return self.entity_factory(id=id)
