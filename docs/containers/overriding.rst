Overriding of containers
------------------------

.. currentmodule:: dependency_injector.containers

Containers can be overridden by other containers. This, actually, means that 
all of the providers from overriding container will override providers with 
the same names in overridden container.

There are two ways to override :py:class:`DeclarativeContainer` with another 
container:

- Use :py:meth:`DeclarativeContainer.override` method.
- Use :py:func:`override` class decorator.

Example of overriding container using :py:meth:`DeclarativeContainer.override` 
method:

.. literalinclude:: ../../examples/containers/override_declarative.py
   :language: python
   :linenos:

Example of overriding container using :py:func:`override` decorator:

.. literalinclude:: ../../examples/containers/override_declarative_decorator.py
   :language: python
   :linenos:

Also there are several useful :py:class:`DeclarativeContainer` methods and 
properties that help to work with container overridings:

- :py:attr:`DeclarativeContainer.overridden` - tuple of all overriding 
  containers.
- :py:meth:`DeclarativeContainer.reset_last_overriding()` - reset last 
  overriding provider for each container providers.
- :py:meth:`DeclarativeContainer.reset_override()` - reset all overridings 
  for each container providers. 

:py:class:`DynamicContainer` has exactly the same functionality, except of 
:py:func:`override` decorator.


.. disqus::
