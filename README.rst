Dependency Injector
===================

Dependency injection framework for Python projects.

+---------------------------------------+-------------------------------------------------------------------------------+
| *PyPi*                                | .. image:: https://img.shields.io/pypi/v/dependency_injector.svg              |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                 |
|                                       |    :alt: Latest Version                                                       |
|                                       | .. image:: https://img.shields.io/pypi/dm/dependency_injector.svg             |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                 |
|                                       |    :alt: Downloads                                                            |
|                                       | .. image:: https://img.shields.io/pypi/l/dependency_injector.svg              |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                 |
|                                       |    :alt: License                                                              |
+---------------------------------------+-------------------------------------------------------------------------------+
| *Python versions and implementations* | .. image:: https://img.shields.io/pypi/pyversions/dependency_injector.svg     |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                 |
|                                       |    :alt: Supported Python versions                                            |
|                                       | .. image:: https://img.shields.io/pypi/implementation/dependency_injector.svg |
|                                       |    :target: https://pypi.python.org/pypi/dependency_injector/                 |
|                                       |    :alt: Supported Python implementations                                     |
+---------------------------------------+-------------------------------------------------------------------------------+
| *Builds and tests coverage*           | .. image:: https://travis-ci.org/rmk135/dependency_injector.svg?branch=master |
|                                       |    :target: https://travis-ci.org/rmk135/dependency_injector                  |
|                                       |    :alt: Build Status                                                         |
|                                       | .. image:: https://coveralls.io/repos/rmk135/dependency_injector/badge.svg    |
|                                       |    :target: https://coveralls.io/r/rmk135/dependency_injector                 |
|                                       |    :alt: Coverage Status                                                      |
+---------------------------------------+-------------------------------------------------------------------------------+

*Dependency Injector* is a dependency injection framework for Python projects. 
It was designed to be unified, developer's friendly tool for managing any kind
of Python objects and their dependencies in formal, pretty way.

Below is a list of some key features and points of *Dependency Injector*
framework:

- Easy, smart, pythonic style.
- Obvious, clear structure.
- Memory efficiency.
- Semantic versioning.

Main idea of *Dependency Injector* is to keep dependencies under control.

Installation
------------

*Dependency Injector* library is available on PyPi_::

    pip install dependency_injector

Documentation
-------------

*Dependency Injector* documentation is hosted on ReadTheDocs:

- `Stable version`_
- `Latest version`_

Examples
--------

.. code-block:: python

    """Concept example of `Dependency Injector`."""

    import sqlite3
    import dependency_injector as di


    class ObjectA(object):

        """Example class ObjectA, that has dependency on database."""

        def __init__(self, db):
            """Initializer."""
            self.db = db


    class ObjectB(object):

        """Example class ObjectB, that has dependencies on ObjectA and database."""

        def __init__(self, a, db):
            """Initializer."""
            self.a = a
            self.db = db


    class Catalog(di.AbstractCatalog):

        """Catalog of providers."""

        database = di.Singleton(sqlite3.Connection,
                                database=':memory:')
        """:type: (di.Provider) -> sqlite3.Connection"""

        object_a_factory = di.Factory(ObjectA,
                                      db=database)
        """:type: (di.Provider) -> ObjectA"""

        object_b_factory = di.Factory(ObjectB,
                                      a=object_a_factory,
                                      db=database)
        """:type: (di.Provider) -> ObjectB"""


    # Catalog static provides.
    a1, a2 = Catalog.object_a_factory(), Catalog.object_a_factory()
    b1, b2 = Catalog.object_b_factory(), Catalog.object_b_factory()

    assert a1 is not a2
    assert b1 is not b2
    assert a1.db is a2.db is b1.db is b2.db is Catalog.database()


    # Example of inline injections.
    @di.inject(a=Catalog.object_a_factory)
    @di.inject(b=Catalog.object_b_factory)
    @di.inject(database=Catalog.database)
    def example(a, b, database):
        """Example callback."""
        assert a.db is b.db is database is Catalog.database()


    example()

You can get more *Dependency Injector* examples in ``/examples`` directory on
GitHub:

    https://github.com/rmk135/dependency_injector


Feedback
--------

Feel free to post questions, bugs, feature requests, proposals etc. on
*Dependency Injector*  GitHub Issues:

    https://github.com/rmk135/dependency_injector/issues

Your feedback is quite important!


.. _PyPi: https://pypi.python.org/pypi/dependency_injector
.. _Stable version: http://dependency_injector.readthedocs.org/en/stable/
.. _Latest version: http://dependency_injector.readthedocs.org/en/latest/
.. _SLOC: http://en.wikipedia.org/wiki/Source_lines_of_code
.. _SOLID: http://en.wikipedia.org/wiki/SOLID_%28object-oriented_design%29
.. _IoC: http://en.wikipedia.org/wiki/Inversion_of_control
.. _dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
