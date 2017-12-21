class UserRepository(object):

    def __init__(self, object_factory, db):
        self.object_factory = object_factory
        self.db = db

    def get(self, id):
        return self.object_factory(id=id)
