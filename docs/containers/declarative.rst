Declarative containers
----------------------

.. currentmodule:: dependency_injector.containers

:py:class:`DeclarativeContainer` is inversion of control container that 
could be defined in declarative manner. It should cover most of the cases 
when list of providers that would be included in container is deterministic 
(container will not change its structure in runtime).

Declarative containers have to extend base declarative container class - 
:py:class:`dependency_injector.containers.DeclarativeContainer`.

Declarative container's providers have to be defined like container's class 
attributes. Every provider in container has name. This name should follow 
``some_provider`` convention, that is standard naming convention for 
attribute names in Python.

.. note::

    Declarative containers have several features that could be useful 
    for some kind of operations on container's providers, please visit API 
    documentation for getting full list of features - 
    :py:class:`dependency_injector.containers.DeclarativeContainer`.

Here is an simple example of defining declarative container with several 
factories:

.. image:: /images/containers/declarative.png
    :width: 85%
    :align: center

.. literalinclude:: ../../examples/containers/declarative.py
   :language: python
   :linenos:

Example of declarative containers inheritance:

.. image:: /images/containers/declarative_inheritance.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/containers/declarative_inheritance.py
   :language: python
   :linenos:

Example of declarative containers's provider injections:

.. image:: /images/containers/declarative_injections.png
    :width: 100%
    :align: center

.. literalinclude:: ../../examples/containers/declarative_injections.py
   :language: python
   :linenos:
