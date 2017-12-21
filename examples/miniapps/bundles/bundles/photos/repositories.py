class PhotoRepository(object):

    def __init__(self, object_factory, fs, db):
        self.object_factory = object_factory
        self.fs = fs
        self.db = db
