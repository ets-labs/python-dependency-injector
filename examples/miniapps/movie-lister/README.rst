Movie lister - a naive example of dependency injection in Python
================================================================

This is a Python implementation of the dependency injection example from Martin Fowler's
article:

    https://www.martinfowler.com/articles/injection.html

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

The output should be something like this for each command:

.. code-block:: bash

   Francis Lawrence movies:
       - Movie(title='The Hunger Games: Mockingjay - Part 2', year=2015, director='Francis Lawrence')
   2016 movies:
       - Movie(title='Rogue One: A Star Wars Story', year=2016, director='Gareth Edwards')
       - Movie(title='The Jungle Book', year=2016, director='Jon Favreau')

Test
----

To run the tests do:

.. code-block:: bash

   pytest movies/tests.py --cov=movies

The output should be something like:

.. code-block::

   platform linux -- Python 3.12.3, pytest-8.3.2, pluggy-1.5.0
   plugins: cov-6.0.0
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
