"""Movie finders module.

This module contains all finder implementations.
"""

import csv


class MovieFinder:
    """Movie finder component.

    Movie finder component is responsible for fetching movies data from
    various storage.
    """

    def __init__(self, movie_model):
        """Initialize instance.

        :param movie_model: Movie model's factory
        :type movie_model: movies.models.Movie
        """
        self._movie_model = movie_model

    def find_all(self):
        """Return all found movies.

        :rtype: list[movies.models.Movie]
        :return: List of movie instances.
        """
        raise NotImplementedError()


class CsvMovieFinder(MovieFinder):
    """Movie finder that fetches movies data from csv file."""

    def __init__(self, movie_model, csv_file_path, delimiter):
        """Initialize instance.

        :param movie_model: Movie model's factory
        :type movie_model: movies.models.Movie

        :param csv_file_path: Path to csv file with movies data
        :type csv_file_path: str

        :param delimiter: Csv file's delimiter
        :type delimiter: str
        """
        self._csv_file_path = csv_file_path
        self._delimiter = delimiter
        super().__init__(movie_model)

    def find_all(self):
        """Return all found movies.

        :rtype: list[movies.models.Movie]
        :return: List of movie instances.
        """
        with open(self._csv_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self._delimiter)
            return [self._movie_model(*row) for row in csv_reader]


class SqliteMovieFinder(MovieFinder):
    """Movie finder that fetches movies data from sqlite database."""

    def __init__(self, movie_model, database):
        """Initialize instance.

        :param movie_model: Movie model's factory
        :type movie_model: (object) -> movies.models.Movie

        :param database: Connection to sqlite database with movies data
        :type database: sqlite3.Connection
        """
        self._database = database
        super().__init__(movie_model)

    def find_all(self):
        """Return all found movies.

        :rtype: list[movies.models.Movie]
        :return: List of movie instances.
        """
        with self._database:
            rows = self._database.execute('SELECT name, year, director '
                                          'FROM movies')
            return [self._movie_model(*row) for row in rows]
