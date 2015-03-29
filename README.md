Objects
=======

Dependency management tool for Python projects.

[![Latest Version](https://pypip.in/version/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)
[![Downloads](https://pypip.in/download/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)
[![Build Status](https://travis-ci.org/rmk135/objects.svg?branch=master)](https://travis-ci.org/rmk135/objects)
[![Coverage Status](https://coveralls.io/repos/rmk135/objects/badge.svg)](https://coveralls.io/r/rmk135/objects)
[![License](https://pypip.in/license/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)
[![Supported Python versions](https://pypip.in/py_versions/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)
[![Supported Python implementations](https://pypip.in/implementation/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)

Introduction
------------

Python ecosystem consists of a big amount of various classes, functions and 
objects that could be used for applications development. Each of them has its 
own role.

Modern Python applications are mostly the composition of well-known open 
source systems, frameworks, libraries and some turnkey functionality.

When application goes bigger, an amount of objects and their dependencies in 
it also increased extremely fast and became hard to maintain.

`Objects` is designed to be developer's friendly tool for managing objects 
and their dependencies in formal, pretty way. Main idea of `Objects` is to 
keep dependencies of Python projects under control.

Entities
--------

- Providers are strategies of accessing to objects.
- Injections are additional instructions, that are used for determining objects 
dependencies.
- Catalogs are named set of providers.

Example
-------

```python
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
```
