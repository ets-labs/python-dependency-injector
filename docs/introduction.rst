Introduction
============

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


.. _SLOC: http://en.wikipedia.org/wiki/Source_lines_of_code
.. _SOLID: http://en.wikipedia.org/wiki/SOLID_%28object-oriented_design%29
.. _IoC: http://en.wikipedia.org/wiki/Inversion_of_control
.. _dependency injection: http://en.wikipedia.org/wiki/Dependency_injection
