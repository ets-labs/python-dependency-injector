# Objects

Dependency management tool for Python projects.

[![Latest Version](https://pypip.in/version/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)
[![Downloads](https://pypip.in/download/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)
[![Build Status](https://travis-ci.org/rmk135/objects.svg?branch=master)](https://travis-ci.org/rmk135/objects)
[![Coverage Status](https://coveralls.io/repos/rmk135/objects/badge.svg)](https://coveralls.io/r/rmk135/objects)
[![License](https://pypip.in/license/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)
[![Supported Python versions](https://pypip.in/py_versions/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)
[![Supported Python implementations](https://pypip.in/implementation/Objects/badge.svg)](https://pypi.python.org/pypi/Objects/)

## Introduction

Python ecosystem consists of a big amount of various classes, functions and 
objects that could be used for applications development. Each of them has its 
own role.

Modern Python applications are mostly the composition of well-known open 
source systems, frameworks, libraries and some turnkey functionality.

When application goes bigger, its amount of objects and their dependencies 
also increased extremely fast and became hard to maintain.

`Objects` is designed to be developer's friendly tool for managing objects 
and their dependencies in formal, pretty way. Main idea of `Objects` is to 
keep dependencies under control.

## Entities

Current section describes main `Objects` entities and their interaction.

### Providers

Providers are strategies of accessing objects.

All providers are callable. They describe how particular objects will be 
provided. For example:

```python
"""`NewInstance` and `Singleton` providers example."""

from objects.providers import NewInstance
from objects.providers import Singleton


# NewInstance provider will create new instance of specified class
# on every call.
new_object = NewInstance(object)

object_1 = new_object()
object_2 = new_object()

assert object_1 is not object_2

# Singleton provider will create new instance of specified class on first call,
# and return same instance on every next call.
single_object = Singleton(object)

single_object_1 = single_object()
single_object_2 = single_object()

assert single_object_1 is single_object_2
```

### Injections

Injections are additional instructions, that are used for determining 
dependencies of objects.

Objects can take dependencies in various forms. Some objects take init 
arguments, other are using attributes or methods to be initialized. Injection, 
in terms of `Objects`, is an instruction how to provide dependency for the 
particular object.

Every Python object could be an injection value. Special case is a `Objects` 
provider as an injection value. In such case, injection value is a result of 
injectable provider call (every time injection is done).

Injections are used by providers.

### Catalogs

Catalogs are named set of providers.

## Example

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
