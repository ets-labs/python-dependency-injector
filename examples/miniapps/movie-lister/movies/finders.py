"""Movie finders module."""

from typing import Callable, List

from .models import Movie
from .storages import MovieStorage


class MovieFinder:

    def __init__(
            self,
            movie_factory: Callable[..., Movie],
            movie_storage: MovieStorage,
    ) -> None:
        self._movie_factory = movie_factory
        self._movie_storage = movie_storage

    def find_all(self) -> List[Movie]:
        return [
            self._movie_factory(*row)
            for row in self._movie_storage.get_all()
        ]
