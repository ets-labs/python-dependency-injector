Objects
=======

Dependency injection framework for Python projects.

+---------------------------------------+-------------------------------------------------------------------+
| *PyPi*                                | .. image:: https://pypip.in/version/Objects/badge.svg             |
|                                       |    :target: https://pypi.python.org/pypi/Objects/                 |
|                                       |    :alt: Latest Version                                           |
|                                       | .. image:: https://pypip.in/download/Objects/badge.svg            |
|                                       |    :target: https://pypi.python.org/pypi/Objects/                 |
|                                       |    :alt: Downloads                                                |
|                                       | .. image:: https://pypip.in/license/Objects/badge.svg             |
|                                       |    :target: https://pypi.python.org/pypi/Objects/                 |
|                                       |    :alt: License                                                  |
+---------------------------------------+-------------------------------------------------------------------+
| *Python versions and implementations* | .. image:: https://pypip.in/py_versions/Objects/badge.svg         |
|                                       |    :target: https://pypi.python.org/pypi/Objects/                 |
|                                       |    :alt: Supported Python versions                                |
|                                       | .. image:: https://pypip.in/implementation/Objects/badge.svg      |
|                                       |    :target: https://pypi.python.org/pypi/Objects/                 |
|                                       |    :alt: Supported Python implementations                         |
+---------------------------------------+-------------------------------------------------------------------+
| *Builds and test coverage*            | .. image:: https://travis-ci.org/rmk135/objects.svg?branch=master |
|                                       |    :target: https://travis-ci.org/rmk135/objects                  |
|                                       |    :alt: Build Status                                             |
|                                       | .. image:: https://coveralls.io/repos/rmk135/objects/badge.svg    |
|                                       |    :target: https://coveralls.io/r/rmk135/objects                 |
|                                       |    :alt: Coverage Status                                          |
+---------------------------------------+-------------------------------------------------------------------+

Introduction
------------

Python ecosystem consists of a big amount of various libraries that contain
different classes and functions that could be used for applications
development. Each of them has its own role.

Modern Python applications are mostly the composition of well-known open
source systems / frameworks / libraries and some turnkey functionality.

When application goes bigger, its complexity and SLOC_ are also increased.
Being driven by SOLID_ (for example), developers often start to split
application's sources into not so big classes, functions and modules. It
always helps, but there is another problem on the horizon.

It sounds like "I have so many classes and functions! They are great, now I can
understand each of them, but it is so hard to see the whole picture! How are
they linked with each other? What dependencies does this class have?". And
this is a key question: "What dependencies do certain class / function have?".
To resolve this issues developers have to go inside with IoC_ principles and
implementation patterns.

One of such IoC_ implementation patterns is called `dependency injection`_.

*Objects* is a dependency injection framework for Python projects.

It was designed to be developer's friendly tool for managing any kind of
Python objects and their dependencies in formal, pretty way.

Main idea of *Objects* is to keep dependencies under control.

Installation
------------

*Objects* library is available on PyPi_::

    pip install objects

Documentation
-------------

*Objects* documentation is hosted on ReadTheDocs:

- `Stable version`_
- `Latest version`_

Examples
--------

.. code-block:: python

    """Concept example of `Objects`."""

    from objects.catalog import AbstractCatalog

    from objects.providers import Singleton
    from objects.providers import NewInstance

    from objects.injections import KwArg
    from objects.injections import Attribute
    from objects.injections import inject

    import sqlite3


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


    class Catalog(AbstractCatalog):

        """Catalog of objects providers."""

        database = Singleton(sqlite3.Connection,
                             KwArg('database', ':memory:'),
                             Attribute('row_factory', sqlite3.Row))
        """:type: (objects.Provider) -> sqlite3.Connection"""

        object_a = NewInstance(ObjectA,
                               KwArg('db', database))
        """:type: (objects.Provider) -> ObjectA"""

        object_b = NewInstance(ObjectB,
                               KwArg('a', object_a),
                               KwArg('db', database))
        """:type: (objects.Provider) -> ObjectB"""


    # Catalog static provides.
    a1, a2 = Catalog.object_a(), Catalog.object_a()
    b1, b2 = Catalog.object_b(), Catalog.object_b()

    assert a1 is not a2
    assert b1 is not b2
    assert a1.db is a2.db is b1.db is b2.db is Catalog.database()


    # Example of inline injections.
    @inject(KwArg('a', Catalog.object_a))
    @inject(KwArg('b', Catalog.object_b))
    @inject(KwArg('database', Catalog.database))
    def example(a, b, database):
        assert a.db is b.db is database is Catalog.database()


    example()

You can get more *Objects* examples in ``/examples`` directory on
GitHub:

    https://github.com/rmk135/objects


Feedback
--------

Feel free to post questions, bugs, feature requests, proposals etc. on
*Objects*  GitHub Issues:

    https://github.com/rmk135/objects/issues

Your feedback is quite important!


.. _PyPi: https://pypi.python.org/pypi/Objects
.. _Stable version: http://objects.readthedocs.org/en/stable/
.. _Latest version: http://objects.readthedocs.org/en/latest/
.. _SLOC: http://en.wikipedia.org/wiki/Source_lines_of_code
.. _SOLID: http://en.wikipedia.org/wiki/SOLID_%28object-oriented_design%29
.. _IoC: http://en.wikipedia.org/wiki/Inversion_of_control
.. _dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
