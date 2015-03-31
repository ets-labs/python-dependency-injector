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

Every Python object could be an injection's value. Special case is a `Objects` 
provider as an injection's value. In such case, injection value is a result of 
injectable provider call (every time injection is done).

Injections are used by providers.

```python
"""`KwArg` and `Attribute` injections example."""

import sqlite3

from objects.providers import Singleton
from objects.providers import NewInstance

from objects.injections import KwArg
from objects.injections import Attribute


class ObjectA(object):

    """ObjectA has dependency on database."""

    def __init__(self, database):
        """Initializer.

        Database dependency need to be injected via init arg."""
        self.database = database

    def get_one(self):
        """Select one from database and return it."""
        return self.database.execute('SELECT 1').fetchone()[0]


# Database and `ObjectA` providers.
database = Singleton(sqlite3.Connection,
                     KwArg('database', ':memory:'),
                     KwArg('timeout', 30),
                     KwArg('detect_types', True),
                     KwArg('isolation_level', 'EXCLUSIVE'),
                     Attribute('row_factory', sqlite3.Row))

object_a = NewInstance(ObjectA,
                       KwArg('database', database))

# Creating several `ObjectA` instances.
object_a_1 = object_a()
object_a_2 = object_a()

# Making some asserts.
assert object_a_1 is not object_a_2
assert object_a_1.database is object_a_2.database
assert object_a_1.get_one() == object_a_2.get_one() == 1
```

### Catalogs

Catalogs are named set of providers.

`Objects` catalogs can be used for grouping of providers by some 
kind of rules. In example below, there are two catalogs: 
`Resources` and `Models`.

`Resources` catalog is used to group all common application resources like 
database connection and various api clients, while `Models` catalog is used 
for application model providers only.

```python
"""Catalogs example."""

import sqlite3
import httplib

from objects.catalog import AbstractCatalog

from objects.providers import Singleton
from objects.providers import NewInstance

from objects.injections import KwArg
from objects.injections import Attribute


class SomeModel(object):

    """SomeModel has dependency on database and api client.

    Dependencies need to be injected via init args.
    """

    def __init__(self, database, api_client):
        """Initializer."""
        self.database = database
        self.api_client = api_client

    def api_request(self):
        """Make api request."""
        self.api_client.request('GET', '/')
        return self.api_client.getresponse()

    def get_one(self):
        """Select one from database and return it."""
        return self.database.execute('SELECT 1').fetchone()[0]


class Resources(AbstractCatalog):

    """Resource providers catalog."""

    database = Singleton(sqlite3.Connection,
                         KwArg('database', ':memory:'),
                         KwArg('timeout', 30),
                         KwArg('detect_types', True),
                         KwArg('isolation_level', 'EXCLUSIVE'),
                         Attribute('row_factory', sqlite3.Row))

    api_client = Singleton(httplib.HTTPConnection,
                           KwArg('host', 'example.com'),
                           KwArg('port', 80),
                           KwArg('timeout', 10))


class Models(AbstractCatalog):

    """Model providers catalog."""

    some_model = NewInstance(SomeModel,
                             KwArg('database', Resources.database),
                             KwArg('api_client', Resources.api_client))


# Creating `SomeModel` instance.
some_model = Models.some_model()

# Making some asserts.
assert some_model.get_one() == 1
assert some_model.api_request().status == 200
```

## Advanced usage

Below you can find some variants of advanced usage of `Objects`.

### Inject decorator

`@inject` decorator could be used for patching any callable with injection.
Any Python object will be injected 'as is', except `Objects` providers, 
that will be called to provide injectable value.


```python
"""`@inject` decorator example."""

from objects.providers import NewInstance

from objects.injections import KwArg
from objects.injections import inject


new_object = NewInstance(object)


@inject(KwArg('object_a', new_object))
@inject(KwArg('some_setting', 1334))
def example_callback(object_a, some_setting):
    """This function has dependencies on object a and b.

    Dependencies are injected using `@inject` decorator.
    """
    assert isinstance(object_a, object)
    assert some_setting == 1334


example_callback()
example_callback()
```

### Overriding providers

Any provider can be overridden by another provider.

Example:

```python
"""Provider overriding example."""

import sqlite3

from objects.providers import Singleton
from objects.providers import NewInstance

from objects.injections import KwArg
from objects.injections import Attribute


class ObjectA(object):

    """ObjectA has dependency on database."""

    def __init__(self, database):
        """Initializer.

        Database dependency need to be injected via init arg."""
        self.database = database

    def get_one(self):
        """Select one from database and return it."""
        return self.database.execute('SELECT 1')


class ObjectAMock(ObjectA):

    """Mock of ObjectA.

    Has no dependency on database.
    """

    def __init__(self):
        """Initializer."""

    def get_one(self):
        """Select one from database and return it.

        Mock makes no database queries and always returns two instead of one.
        """
        return 2


# Database and `ObjectA` providers.
database = Singleton(sqlite3.Connection,
                     KwArg('database', ':memory:'),
                     KwArg('timeout', 30),
                     KwArg('detect_types', True),
                     KwArg('isolation_level', 'EXCLUSIVE'),
                     Attribute('row_factory', sqlite3.Row))

object_a = NewInstance(ObjectA,
                       KwArg('database', database))


# Overriding `ObjectA` provider with `ObjectAMock` provider.
object_a.override(NewInstance(ObjectAMock))

# Creating several `ObjectA` instances.
object_a_1 = object_a()
object_a_2 = object_a()

# Making some asserts.
assert object_a_1 is not object_a_2
assert object_a_1.get_one() == object_a_2.get_one() == 2
```

### Overriding catalogs

Any catalog can be overridden by another catalog.

Example:

```python
"""Catalog overriding example."""

import sqlite3

from objects.catalog import AbstractCatalog
from objects.catalog import override

from objects.providers import Singleton
from objects.providers import NewInstance

from objects.injections import KwArg
from objects.injections import Attribute


class ObjectA(object):

    """ObjectA has dependency on database."""

    def __init__(self, database):
        """Initializer.

        Database dependency need to be injected via init arg."""
        self.database = database

    def get_one(self):
        """Select one from database and return it."""
        return self.database.execute('SELECT 1')


class ObjectAMock(ObjectA):

    """Mock of ObjectA.

    Has no dependency on database.
    """

    def __init__(self):
        """Initializer."""

    def get_one(self):
        """Select one from database and return it.

        Mock makes no database queries and always returns two instead of one.
        """
        return 2


class Catalog(AbstractCatalog):

    """Catalog of objects providers."""

    database = Singleton(sqlite3.Connection,
                         KwArg('database', ':memory:'),
                         KwArg('timeout', 30),
                         KwArg('detect_types', True),
                         KwArg('isolation_level', 'EXCLUSIVE'),
                         Attribute('row_factory', sqlite3.Row))

    object_a = NewInstance(ObjectA,
                           KwArg('database', database))


@override(Catalog)
class SandboxCatalog(Catalog):

    """Sandbox objects catalog with some mocks that overrides Catalog."""

    object_a = NewInstance(ObjectAMock)


# Creating several `ObjectA` instances.
object_a_1 = Catalog.object_a()
object_a_2 = Catalog.object_a()

# Making some asserts.
assert object_a_1 is not object_a_2
assert object_a_1.get_one() == object_a_2.get_one() == 2
```
