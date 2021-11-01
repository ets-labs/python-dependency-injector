"""Handlers module."""

from .repositories import RatingRepository


class CommandHandler:
    def __init__(self, rating_repo: RatingRepository):
        self.rating_repo = rating_repo

    def save_rating(self):
        print("Saving rating")

    def something_else(self):
        print("Doing something else")
