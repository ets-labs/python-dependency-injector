"""Analytics services module."""


class AggregationService:

    def __init__(self, user_repository, photo_repository):
        self.user_repository = user_repository
        self.photo_repository = photo_repository
