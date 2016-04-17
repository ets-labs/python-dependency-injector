"""Movie finders module.

This module contains all finder implementations.
"""

import csv


class MovieFinder(object):
    """Movie finder component.

    Movie finder component is responsible for fetching movies data from
    different storages.
    """

    def __init__(self, movie_model):
        """Initializer.

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

    def __init__(self, movie_model, csv_file, delimeter):
        """Initializer.

        :param movie_model: Movie model's factory
        :type movie_model: movies.models.Movie

        :param csv_file: Path to csv file with movies data
        :type csv_file: str

        :param delimeter: Csv file's delimeter
        :type delimeter: str
        """
        self._csv_file = csv_file
        self._delimeter = delimeter
        super(CsvMovieFinder, self).__init__(movie_model)

    def find_all(self):
        """Return all found movies.

        :rtype: list[movies.models.Movie]
        :return: List of movie instances.
        """
        with open(self._csv_file) as csv_file:
            reader = csv.reader(csv_file, delimiter=self._delimeter)
            return [self._movie_model(*row) for row in reader]


class SqliteMovieFinder(MovieFinder):
    """Movie finder that fetches movies data from sqlite database."""

    def __init__(self, movie_model, database):
        """Initializer.

        :param movie_model: Movie model's factory
        :type movie_model: (object) -> movies.models.Movie

        :param database: Connection to sqlite database with movies data
        :type database: sqlite3.Connection
        """
        self._database = database
        super(SqliteMovieFinder, self).__init__(movie_model)

    def find_all(self):
        """Return all found movies.

        :rtype: list[movies.models.Movie]
        :return: List of movie instances.
        """
        with self._database:
            rows = self._database.execute('SELECT name, year, director '
                                          'FROM movies')
            return [self._movie_model(*row) for row in rows]
