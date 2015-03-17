Objects
=======

Python catalogs of objects providers

[![Latest Version](https://pypip.in/version/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)
[![Downloads](https://pypip.in/download/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)
[![Build Status](https://travis-ci.org/rmk135/objects.svg?branch=master)](https://travis-ci.org/rmk135/objects)
[![Coverage Status](https://coveralls.io/repos/rmk135/objects/badge.svg)](https://coveralls.io/r/rmk135/objects)
[![License](https://pypip.in/license/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)

Example:

```python
"""Concept example of Objects."""

from objects import AbstractCatalog

from objects.providers import Singleton
from objects.providers import NewInstance

from objects.injections import InitArg
from objects.injections import Attribute

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
                         InitArg('database', ':memory:'),
                         Attribute('row_factory', sqlite3.Row))
    """:type: (objects.Provider) -> sqlite3.Connection"""

    object_a = NewInstance(ObjectA,
                           InitArg('db', database))
    """:type: (objects.Provider) -> ObjectA"""

    object_b = NewInstance(ObjectB,
                           InitArg('a', object_a),
                           InitArg('db', database))
    """:type: (objects.Provider) -> ObjectB"""


# Catalog static provides.
a1, a2 = Catalog.object_a(), Catalog.object_a()
b1, b2 = Catalog.object_b(), Catalog.object_b()

# Some asserts.
assert a1 is not a2
assert b1 is not b2
assert a1.db is a2.db is b1.db is b2.db is Catalog.database()
```
