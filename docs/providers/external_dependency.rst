External dependency providers
-----------------------------

``di.ExternalDependency`` provider can be useful for development of
self-sufficient libraries / modules / applications that has required external
dependencies.

For example, you have created self-sufficient library / module / application,
that has dependency on *database connection*.

Second step you want to do is to make this software component to be easy
reusable by wide amount of developers and to be easily integrated into many
applications.

It may be good idea, to move all external dependencies (like
*database connection*) to the top level and make them to be injected on your
software component's initialization. It will make third party developers feel
themselves free about integration of yours component in their applications,
because they would be able to find right place / right way for doing this
in their application's architectures.

At the same time, you can be sure, that your external dependency will be
satisfied with appropriate instance.

Example:

.. note::

    Class ``UserService`` is a part of some library. ``UserService`` has
    dependency on database connection, which can be satisfied with any
    DBAPI 2.0 database connection. Being a self-sufficient library,
    ``UserService`` doesn't hardcode any kind of database management logic.
    Instead of this, ``UserService`` has external dependency, that has to
    be satisfied by cleint's code, out of library's scope.

.. image:: /images/providers/external_dependency.png

.. literalinclude:: ../../examples/providers/external_dependency.py
   :language: python
