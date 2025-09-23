"""Movie finders module."""

import csv
import sqlite3
from typing import Callable, List

from .entities import Movie


class MovieFinder:

    def __init__(self, movie_factory: Callable[..., Movie]) -> None:
        self._movie_factory = movie_factory

    def find_all(self) -> List[Movie]:
        raise NotImplementedError()


class CsvMovieFinder(MovieFinder):

    def __init__(
            self,
            movie_factory: Callable[..., Movie],
            path: str,
            delimiter: str,
    ) -> None:
        self._csv_file_path = path
        self._delimiter = delimiter
        super().__init__(movie_factory)

    def find_all(self) -> List[Movie]:
        with open(self._csv_file_path, newline="") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self._delimiter)
            return [self._movie_factory(*row) for row in csv_reader]


class SqliteMovieFinder(MovieFinder):

    def __init__(
            self,
            movie_factory: Callable[..., Movie],
            path: str,
    ) -> None:
        self._database = sqlite3.connect(path)
        super().__init__(movie_factory)

    def find_all(self) -> List[Movie]:
        with self._database as db:
            rows = db.execute("SELECT title, year, director FROM movies")
            return [self._movie_factory(*row) for row in rows]
