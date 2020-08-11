Movie lister - a naive example of dependency injection in Python
================================================================

This is a Python implementation of the dependency injection example from Martin Fowler's
article about dependency injection and inversion of control:

    http://www.martinfowler.com/articles/injection.html

Create virtual environment:

.. code-block:: bash

   virtualenv venv
   . venv/bin/activate

Install requirements:

.. code-block:: bash

    pip install -r requirements.txt

To run the application do:

.. code-block:: bash

   MOVIE_STORAGE_TYPE=csv python -m movies
   MOVIE_STORAGE_TYPE=sqlite python -m movies

The output should be something like:

.. code-block:: bash

   [Movie(name='The Hunger Games: Mockingjay - Part 2', year=2015, director='Francis Lawrence')]
   [Movie(name='The 33', year=2015, director='Patricia Riggen')]
   [Movie(name='Star Wars: Episode VII - The Force Awakens', year=2015, director='JJ Abrams')]
   [Movie(name='The Hunger Games: Mockingjay - Part 2', year=2015, director='Francis Lawrence'), Movie(name='The 33', year=2015, director='Patricia Riggen'), Movie(name='Star Wars: Episode VII - The Force Awakens', year=2015, director='JJ Abrams')]

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
   movies/__main__.py        15     15     0%
   movies/containers.py       9      0   100%
   movies/finders.py          9      0   100%
   movies/fixtures.py         1      0   100%
   movies/listers.py          8      0   100%
   movies/models.py           7      1    86%
   movies/storages.py        32     17    47%
   movies/tests.py           24      0   100%
   ------------------------------------------
   TOTAL                    105     33    69%
