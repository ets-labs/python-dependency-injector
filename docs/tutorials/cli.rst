.. _cli-tutorial:

CLI application tutorial
========================

.. meta::
   :keywords: Python,CLI,Tutorial,Education,Web,Example,DI,Dependency injection,IoC,
              Inversion of control,Refactoring,Tests,Unit tests,Pytest,py.test
   :description: This tutorial shows how to build a CLI application following the dependency
                 injection principle. You will create the CLI script, use CSV files and sqlite
                 database, cover the application with the unit the tests and make some refactoring.

This tutorial shows how to build a CLI application following the dependency injection
principle.

Start from the scratch or jump to the section:

.. contents::
   :local:
   :backlinks: none

You can find complete project on the
`Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/movie-lister>`_.

What are we going to build?
---------------------------

We will build a CLI application that helps to search for the movies. Let's call it Movie Lister.

How does Movie Lister work?

- There is a movies database
- Each movie has next fields:
    - Title
    - Year of the release
    - Director's name
- The database is distributed in two formats:
   - Csv
   - Sqlite
- Application uses the movies database to search for the movies
- Application can search for the movies by:
    - Director's name
    - Year of the release
- Other database formats can be added later

Movie Lister is a naive example from Martin Fowler's article about the dependency injection and
inversion of control:

    https://www.martinfowler.com/articles/injection.html

Here is a class diagram of the Movie Lister application:

.. image:: cli-images/classes-01.png

The responsibilities are split next way:

- ``MovieLister`` - is responsible for the search
- ``MovieFinder`` - is responsible for the fetching from the database
- ``Movie`` - the movie entity

Prepare the environment
-----------------------

Let's create the environment for the project.

First we need to create a project folder:

.. code-block:: bash

   mkdir movie-lister-tutorial
   cd movie-lister-tutorial

Now let's create and activate virtual environment:

.. code-block:: bash

   python3 -m venv venv
   . venv/bin/activate

Project layout
--------------

Create next structure in the project root directory. All files are empty. That's ok for now.

Initial project layout:

.. code-block:: bash

   ./
   ├── movies/
   │   ├── __init__.py
   │   ├── __main__.py
   │   └── containers.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

Move on to the project requirements.

Install the requirements
------------------------

Now it's time to install the project requirements. We will use next packages:

- ``dependency-injector`` - the dependency injection framework
- ``pyyaml`` - the YAML files parsing library, used for the reading of the configuration files
- ``pytest`` - the test framework
- ``pytest-cov`` - the helper library for measuring the test coverage

Put next lines into the ``requirements.txt`` file:

.. code-block:: bash

   dependency-injector
   pyyaml
   pytest
   pytest-cov

and run next in the terminal:

.. code-block:: bash

   pip install -r requirements.txt

The requirements are setup. Now we will add the fixtures.

Fixtures
--------

In this section we will add the fixtures.

We will create a script that creates database files.

First add the folder ``data/`` in the root of the project and then add the file
``fixtures.py`` inside of it:

.. code-block:: bash
   :emphasize-lines: 2-3

   ./
   ├── data/
   │   └── fixtures.py
   ├── movies/
   │   ├── __init__.py
   │   ├── __main__.py
   │   └── containers.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

Second put next in the ``fixtures.py``:

.. code-block:: python

   """Fixtures module."""

   import csv
   import sqlite3
   import pathlib


   SAMPLE_DATA = [
       ("The Hunger Games: Mockingjay - Part 2", 2015, "Francis Lawrence"),
       ("Rogue One: A Star Wars Story", 2016, "Gareth Edwards"),
       ("The Jungle Book", 2016, "Jon Favreau"),
   ]

   FILE = pathlib.Path(__file__)
   DIR = FILE.parent
   CSV_FILE = DIR / "movies.csv"
   SQLITE_FILE = DIR / "movies.db"


   def create_csv(movies_data, path):
       with open(path, "w") as opened_file:
           writer = csv.writer(opened_file)
           for row in movies_data:
               writer.writerow(row)


   def create_sqlite(movies_data, path):
       with sqlite3.connect(path) as db:
           db.execute(
               "CREATE TABLE IF NOT EXISTS movies "
               "(title text, year int, director text)"
           )
           db.execute("DELETE FROM movies")
           db.executemany("INSERT INTO movies VALUES (?,?,?)", movies_data)


   def main():
       create_csv(SAMPLE_DATA, CSV_FILE)
       create_sqlite(SAMPLE_DATA, SQLITE_FILE)
       print("OK")


   if __name__ == "__main__":
       main()

Now run in the terminal:

.. code-block:: bash

   python data/fixtures.py

You should see:

.. code-block:: bash

   OK

Check that files ``movies.csv`` and ``movies.db`` have appeared in the ``data/`` folder:

.. code-block:: bash
   :emphasize-lines: 4-5

   ./
   ├── data/
   │   ├── fixtures.py
   │   ├── movies.csv
   │   └── movies.db
   ├── movies/
   │   ├── __init__.py
   │   ├── __main__.py
   │   └── containers.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

Fixtures are created. Let's move on.

Container
---------

In this section we will add the main part of our application - the container.

Container will keep all of the application components and their dependencies.

Edit ``containers.py``:

.. code-block:: python

   """Containers module."""

   from dependency_injector import containers


   class Container(containers.DeclarativeContainer):
       ...

Container is empty for now. We will add the providers in the following sections.

Let's also create the ``main()`` function. Its responsibility is to run our application. For now
it will just do nothing.

Edit ``__main__.py``:

.. code-block:: python

   """Main module."""

   from .containers import Container


   def main() -> None:
       ...


   if __name__ == "__main__":
       container = Container()

       main()

Csv finder
----------

In this section we will build everything we need for working with the csv file formats.

We will add:

- The ``Movie`` entity
- The ``MovieFinder`` base class
- The ``CsvMovieFinder`` finder implementation
- The ``MovieLister`` class

After each step we will add the provider to the container.

.. image:: cli-images/classes-02.png

Create the ``entities.py`` in the ``movies`` package:

.. code-block:: bash
   :emphasize-lines: 10

   ./
   ├── data/
   │   ├── fixtures.py
   │   ├── movies.csv
   │   └── movies.db
   ├── movies/
   │   ├── __init__.py
   │   ├── __main__.py
   │   ├── containers.py
   │   └── entities.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: python

   """Movie entities module."""


   class Movie:

       def __init__(self, title: str, year: int, director: str):
           self.title = str(title)
           self.year = int(year)
           self.director = str(director)

       def __repr__(self):
           return "{0}(title={1}, year={2}, director={3})".format(
               self.__class__.__name__,
               repr(self.title),
               repr(self.year),
               repr(self.director),
           )

Now we need to add the ``Movie`` factory to the container. We need to add import of the
``providers`` module from the ``dependency_injector`` package, import ``entities`` module.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 3,5,10

   """Containers module."""

   from dependency_injector import containers, providers

   from . import entities


   class Container(containers.DeclarativeContainer):

       movie = providers.Factory(entities.Movie)

.. note::

   Don't forget to remove the Ellipsis ``...`` from the container. We don't need it anymore
   since we container is not empty.

Let's move on to the finders.

Create the ``finders.py`` in the ``movies`` package:

.. code-block:: bash
   :emphasize-lines: 11

   ./
   ├── data/
   │   ├── fixtures.py
   │   ├── movies.csv
   │   └── movies.db
   ├── movies/
   │   ├── __init__.py
   │   ├── __main__.py
   │   ├── containers.py
   │   ├── entities.py
   │   └── finders.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: python

   """Movie finders module."""

   import csv
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
           with open(self._csv_file_path) as csv_file:
               csv_reader = csv.reader(csv_file, delimiter=self._delimiter)
               return [self._movie_factory(*row) for row in csv_reader]

Now let's add the csv finder into the container.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 5,10,14-19

   """Containers module."""

   from dependency_injector import containers, providers

   from . import finders, entities


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(yaml_files=["config.yml"])

       movie = providers.Factory(entities.Movie)

       csv_finder = providers.Singleton(
           finders.CsvMovieFinder,
           movie_factory=movie.provider,
           path=config.finder.csv.path,
           delimiter=config.finder.csv.delimiter,
       )

The csv finder needs the movie factory. It needs it to create the ``Movie`` entities when
reads the csv rows. To provide the factory we use ``.provider`` factory attribute.
This is also called the delegation of the provider. If we just pass the movie factory
as the dependency, it will be called when csv finder is created and the ``Movie`` instance will
be injected. With the ``.provider`` attribute the provider itself will be injected.

The csv finder also has a few dependencies on the configuration options. We added a configuration
provider to provide these dependencies and specified the location of the configuration file.
The configuration provider will parse the configuration file when we create a container instance.

Not let's define the configuration values.

Edit ``config.yml``:

.. code-block:: yaml

   finder:

     csv:
       path: "data/movies.csv"
       delimiter: ","

The configuration file is ready. Move on to the lister.

Create the ``listers.py`` in the ``movies`` package:

.. code-block:: bash
   :emphasize-lines: 12

   ./
   ├── data/
   │   ├── fixtures.py
   │   ├── movies.csv
   │   └── movies.db
   ├── movies/
   │   ├── __init__.py
   │   ├── __main__.py
   │   ├── containers.py
   │   ├── entities.py
   │   ├── finders.py
   │   └── listers.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: python

   """Movie listers module."""

   from .finders import MovieFinder


   class MovieLister:

       def __init__(self, movie_finder: MovieFinder):
           self._movie_finder = movie_finder

       def movies_directed_by(self, director):
           return [
               movie for movie in self._movie_finder.find_all()
               if movie.director == director
           ]

       def movies_released_in(self, year):
           return [
               movie for movie in self._movie_finder.find_all()
               if movie.year == year
           ]

and edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 5,21-24

   """Containers module."""

   from dependency_injector import containers, providers

   from . import finders, listers, entities


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(yaml_files=["config.yml"])

       movie = providers.Factory(entities.Movie)

       csv_finder = providers.Singleton(
           finders.CsvMovieFinder,
           movie_factory=movie.provider,
           path=config.finder.csv.path,
           delimiter=config.finder.csv.delimiter,
       )

       lister = providers.Factory(
           listers.MovieLister,
           movie_finder=csv_finder,
       )

All the components are created and added to the container.

Let's inject the ``lister`` into the  ``main()`` function.

Edit ``__main__.py``:

.. code-block:: python
   :emphasize-lines: 3-5,9-10,16

   """Main module."""

   from dependency_injector.wiring import Provide, inject

   from .listers import MovieLister
   from .containers import Container


   @inject
   def main(lister: MovieLister = Provide[Container.lister]) -> None:
       ...


   if __name__ == "__main__":
       container = Container()
       container.wire(modules=[__name__])

       main()

Now when we call ``main()`` the container will assemble and inject the movie lister.

Let's add some payload to ``main()`` function. It will list movies directed by
Francis Lawrence and movies released in 2016.

Edit ``__main__.py``:

.. code-block:: python
   :emphasize-lines: 11-17

   """Main module."""

   from dependency_injector.wiring import Provide, inject

   from .listers import MovieLister
   from .containers import Container


   @inject
   def main(lister: MovieLister = Provide[Container.lister]) -> None:
       print("Francis Lawrence movies:")
       for movie in lister.movies_directed_by("Francis Lawrence"):
           print("\t-", movie)

       print("2016 movies:")
       for movie in lister.movies_released_in(2016):
           print("\t-", movie)


   if __name__ == "__main__":
       container = Container()
       container.wire(modules=[__name__])

       main()

All set. Now we run the application.

Run in the terminal:

.. code-block:: bash

   python -m movies

You should see:

.. code-block:: plain

   Francis Lawrence movies:
       - Movie(title='The Hunger Games: Mockingjay - Part 2', year=2015, director='Francis Lawrence')
   2016 movies:
       - Movie(title='Rogue One: A Star Wars Story', year=2016, director='Gareth Edwards')
       - Movie(title='The Jungle Book', year=2016, director='Jon Favreau')

Our application can work with the movies database in the csv format. We also want to support
the sqlite format. We will deal with it in the next section.

Sqlite finder
-------------

In this section we will add another type of the finder - the sqlite finder.

Let's get to work.

Edit ``finders.py``:

.. code-block:: python
   :emphasize-lines: 4,37-50

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
           with open(self._csv_file_path) as csv_file:
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

Now we need to add the sqlite finder to the container and update lister's dependency to use it.

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 21-25,29

   """Containers module."""

   from dependency_injector import containers, providers

   from . import finders, listers, entities


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(yaml_files=["config.yml"])

       movie = providers.Factory(entities.Movie)

       csv_finder = providers.Singleton(
           finders.CsvMovieFinder,
           movie_factory=movie.provider,
           path=config.finder.csv.path,
           delimiter=config.finder.csv.delimiter,
       )

       sqlite_finder = providers.Singleton(
           finders.SqliteMovieFinder,
           movie_factory=movie.provider,
           path=config.finder.sqlite.path,
       )

       lister = providers.Factory(
           listers.MovieLister,
           movie_finder=sqlite_finder,
       )

The sqlite finder has a dependency on the configuration option. Let's update the configuration
file.

Edit ``config.yml``:

.. code-block:: yaml
   :emphasize-lines: 7-8

   finder:

     csv:
       path: "data/movies.csv"
       delimiter: ","

     sqlite:
       path: "data/movies.db"

All is ready. Let's check.

Run in the terminal:

.. code-block:: bash

   python -m movies

You should see:

.. code-block:: plain

   Francis Lawrence movies:
       - Movie(title='The Hunger Games: Mockingjay - Part 2', year=2015, director='Francis Lawrence')
   2016 movies:
       - Movie(title='Rogue One: A Star Wars Story', year=2016, director='Gareth Edwards')
       - Movie(title='The Jungle Book', year=2016, director='Jon Favreau')

Our application now supports both formats: csv files and sqlite databases. Every time when we
need to work with the different format we need to make a code change in the container. We will
improve this in the next section.

Selector
--------

In this section we will make our application more flexible.

The code change will not be needed to switch between csv and sqlite formats. We implement the
switch based on the environment variable ``MOVIE_FINDER_TYPE``:

- When ``MOVIE_FINDER_TYPE=csv`` application uses csv finder.
- When ``MOVIE_FINDER_TYPE=sqlite`` application uses sqlite finder.

We will use the ``Selector`` provider. It selects the provider based on the configuration option
(docs - :ref:`selector-provider`).

Edit ``containers.py``:

.. code-block:: python
   :emphasize-lines: 27-31,35

   """Containers module."""

   from dependency_injector import containers, providers

   from . import finders, listers, entities


   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(yaml_files=["config.yml"])

       movie = providers.Factory(entities.Movie)

       csv_finder = providers.Singleton(
           finders.CsvMovieFinder,
           movie_factory=movie.provider,
           path=config.finder.csv.path,
           delimiter=config.finder.csv.delimiter,
       )

       sqlite_finder = providers.Singleton(
           finders.SqliteMovieFinder,
           movie_factory=movie.provider,
           path=config.finder.sqlite.path,
       )

       finder = providers.Selector(
           config.finder.type,
           csv=csv_finder,
           sqlite=sqlite_finder,
       )

       lister = providers.Factory(
           listers.MovieLister,
           movie_finder=finder,
       )

The switch is the ``config.finder.type`` option. When its value is ``csv``, the provider with the
``csv`` key is used. The same is for ``sqlite``.

Now we need to read the value of the ``config.finder.type`` option from the environment variable
``MOVIE_FINDER_TYPE``.

Edit ``__main__.py``:

.. code-block:: python
   :emphasize-lines: 22

   """Main module."""

   from dependency_injector.wiring import Provide, inject

   from .listers import MovieLister
   from .containers import Container


   @inject
   def main(lister: MovieLister = Provide[Container.lister]) -> None:
       print("Francis Lawrence movies:")
       for movie in lister.movies_directed_by("Francis Lawrence"):
           print("\t-", movie)

       print("2016 movies:")
       for movie in lister.movies_released_in(2016):
           print("\t-", movie)


   if __name__ == "__main__":
       container = Container()
       container.config.finder.type.from_env("MOVIE_FINDER_TYPE")
       container.wire(modules=[sys.modules[__name__]])

       main()

Done.

Run in the terminal line by line:

.. code-block:: bash

   MOVIE_FINDER_TYPE=csv python -m movies
   MOVIE_FINDER_TYPE=sqlite python -m movies

The output should be similar for each command:

.. code-block:: plain

   Francis Lawrence movies:
       - Movie(title='The Hunger Games: Mockingjay - Part 2', year=2015, director='Francis Lawrence')
   2016 movies:
       - Movie(title='Rogue One: A Star Wars Story', year=2016, director='Gareth Edwards')
       - Movie(title='The Jungle Book', year=2016, director='Jon Favreau')

In the next section we will add some tests.

Tests
-----

It would be nice to add some tests. Let's do it.

We will use `pytest <https://docs.pytest.org/en/stable/>`_ and
`coverage <https://coverage.readthedocs.io/>`_.

Create ``tests.py`` in the ``movies`` package:

.. code-block:: bash
   :emphasize-lines: 13

   ./
   ├── data/
   │   ├── fixtures.py
   │   ├── movies.csv
   │   └── movies.db
   ├── movies/
   │   ├── __init__.py
   │   ├── __main__.py
   │   ├── containers.py
   │   ├── entities.py
   │   ├── finders.py
   │   ├── listers.py
   │   └── tests.py
   ├── venv/
   ├── config.yml
   └── requirements.txt

and put next into it:

.. code-block:: python
   :emphasize-lines: 36,51

   """Tests module."""

   from unittest import mock

   import pytest

   from .containers import Container


   @pytest.fixture
   def container():
       container = Container(
           config={
               "finder": {
                   "type": "csv",
                   "csv": {
                       "path": "/fake-movies.csv",
                       "delimiter": ",",
                   },
                   "sqlite": {
                       "path": "/fake-movies.db",
                   },
               },
           },
       )
       return container


   def test_movies_directed_by(container):
       finder_mock = mock.Mock()
       finder_mock.find_all.return_value = [
           container.movie("The 33", 2015, "Patricia Riggen"),
           container.movie("The Jungle Book", 2016, "Jon Favreau"),
       ]

       with container.finder.override(finder_mock):
           lister = container.lister()
           movies = lister.movies_directed_by("Jon Favreau")

       assert len(movies) == 1
       assert movies[0].title == "The Jungle Book"


   def test_movies_released_in(container):
       finder_mock = mock.Mock()
       finder_mock.find_all.return_value = [
           container.movie("The 33", 2015, "Patricia Riggen"),
           container.movie("The Jungle Book", 2016, "Jon Favreau"),
       ]

       with container.finder.override(finder_mock):
           lister = container.lister()
           movies = lister.movies_released_in(2015)

       assert len(movies) == 1
       assert movies[0].title == "The 33"

Run in the terminal:

.. code-block:: bash

   pytest movies/tests.py --cov=movies

You should see:

.. code-block::

   platform darwin -- Python 3.10.0, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
   plugins: cov-3.0.0
   collected 2 items

   movies/tests.py ..                                              [100%]

   ---------- coverage: platform darwin, python 3.10 -----------
   Name                   Stmts   Miss  Cover
   ------------------------------------------
   movies/__init__.py         0      0   100%
   movies/__main__.py        16     16     0%
   movies/containers.py       9      0   100%
   movies/entities.py         7      1    86%
   movies/finders.py         26     13    50%
   movies/listers.py          8      0   100%
   movies/tests.py           23      0   100%
   ------------------------------------------
   TOTAL                     89     30    66%

.. note::

   Take a look at the highlights in the ``tests.py``.

   We use ``.override()`` method of the ``finder`` provider. Provider is overridden by the mock.
   Every time when any other provider will request ``finder`` provider to provide the dependency,
   the mock will be returned. So when we call the ``lister`` provider, the ``MovieLister``
   instance is created with the mock, not an actual ``MovieFinder``.

Conclusion
----------

In this tutorial we've built a CLI application following the dependency injection principle.
We've used the ``Dependency Injector`` as a dependency injection framework.

With a help of :ref:`containers` and :ref:`providers` we have defined how to assemble application components.

``Selector`` provider served as a switch for selecting the database format based on a configuration.
:ref:`configuration-provider` helped to deal with reading a YAML file and environment variables.

We used :ref:`wiring` feature to inject the dependencies into the ``main()`` function.
:ref:`provider-overriding` feature helped in testing.

We kept all the dependencies injected explicitly. This will help when you need to add or
change something in future.

You can find complete project on the
`Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/movie-lister>`_.

What's next?

- Look at the other :ref:`tutorials`
- Know more about the :ref:`providers`
- Go to the :ref:`contents`

.. include:: ../sponsor.rst

.. disqus::
