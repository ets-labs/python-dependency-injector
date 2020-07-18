Movie lister naive example
--------------------------

.. meta::
   :description: Movie lister - is a naive example of dependency injection and 
                 inversion of control containers on Python. Original example 
                 was taken from Martin Fowler's article about dependency 
                 injection and inversion of control.

This naive example was taken from Martin Fowler's article about dependency 
injection and inversion of control: http://www.martinfowler.com/articles/injection.html

Like Martin says:

.. pull-quote::

    *Like all of my examples it's one of those super-simple examples; 
    small enough to be unreal, but hopefully enough for you to visualize 
    what's going on without falling into the bog of a real example.*

While original Martin's MovieLister example was a bit modified here, it 
makes sense to provide some description. So, the idea of this example is to 
create ``movies`` library that can be configured to work with different 
movie databases (csv, sqlite, etc...) and provide 2 main features:

1. List all movies that were directed by certain person.
2. List all movies that were released in certain year.

Also this example contains 3 mini applications that are based on ``movies`` 
library:

1. ``app_csv.py`` - list movies by certain criteria from csv file database.
2. ``app_db.py`` - list movies by certain criteria from sqlite database.
3. ``app_db_csv.py`` - list movies by certain criteria from csv file and 
   sqlite databases.

Instructions for running:

.. code-block:: bash

    python app_csv.py
    python app_db.py
    python app_db_csv.py


Full code of example could be found on GitHub_. 

Movies library
~~~~~~~~~~~~~~

Classes diagram:

.. image:: /images/miniapps/movie_lister/classes.png
    :width: 100%
    :align: center


Movies library structure:

.. code-block:: bash

    /movies
        /__init__.py
        /finders.py
        /listers.py
        /models.py


Listing of ``movies/__init__.py``:

.. literalinclude:: ../../examples/miniapps/movie_lister/movies/__init__.py
   :language: python

Example application
~~~~~~~~~~~~~~~~~~~

Example application structure:

.. code-block:: bash

    /example
        /__init__.py
        /db.py
        /main.py

Listing of ``examples/main.py``:

.. literalinclude:: ../../examples/miniapps/movie_lister/example/main.py
   :language: python

Listing of ``examples/db.py``:

.. literalinclude:: ../../examples/miniapps/movie_lister/example/db.py
   :language: python

Csv application
~~~~~~~~~~~~~~~

Listing of ``app_csv.py``:

.. literalinclude:: ../../examples/miniapps/movie_lister/app_csv.py
   :language: python

Database application
~~~~~~~~~~~~~~~~~~~~

Listing of ``app_db.py``:

.. literalinclude:: ../../examples/miniapps/movie_lister/app_db.py
   :language: python

Csv and database application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listing of ``app_db_csv.py``:

.. literalinclude:: ../../examples/miniapps/movie_lister/app_db_csv.py
   :language: python


.. disqus::


.. _GitHub: https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/movie_lister
