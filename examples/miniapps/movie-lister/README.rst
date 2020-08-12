Movie lister - a naive example of dependency injection in Python
================================================================

This is a Python implementation of the dependency injection example from Martin Fowler's
article:

    http://www.martinfowler.com/articles/injection.html

Run
---

Create a virtual environment:

.. code-block:: bash

   virtualenv venv
   . venv/bin/activate

Install the requirements:

.. code-block:: bash

    pip install -r requirements.txt

To create the fixtures do:

.. code-block:: bash

   python data/fixtures.py

To run the application do:

.. code-block:: bash

   MOVIE_FINDER_TYPE=csv python -m movies
   MOVIE_FINDER_TYPE=sqlite python -m movies

The output should be something like:

.. code-block:: bash

   Francis Lawrence movies: [Movie(name='The Hunger Games: Mockingjay - Part 2', year=2015, director='Francis Lawrence')]
   2016 movies: [Movie(name='Rogue One: A Star Wars Story', year=2016, director='Gareth Edwards'), Movie(name='The Jungle Book', year=2016, director='Jon Favreau')]

Test
----

To run the tests do:

.. code-block:: bash

   pytest movies/tests.py --cov=movies

The output should be something like:

.. code-block::

   platform darwin -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
   plugins: cov-2.10.0
   collected 2 items

   movies/tests.py ..                                              [100%]

   ---------- coverage: platform darwin, python 3.8.3-final-0 -----------
   Name                   Stmts   Miss  Cover
   ------------------------------------------
   movies/__init__.py         0      0   100%
   movies/__main__.py        10     10     0%
   movies/containers.py       9      0   100%
   movies/entities.py         7      1    86%
   movies/finders.py         26     13    50%
   movies/listers.py          8      0   100%
   movies/tests.py           24      0   100%
   ------------------------------------------
   TOTAL                     84     24    71%
