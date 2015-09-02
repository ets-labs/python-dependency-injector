Factory providers
-----------------

``di.Factory`` provider creates new instance of specified class on every call.

Nothing could be better than brief example:

.. image:: /images/providers/factory.png
    :width: 80%
    :align: center

.. literalinclude:: ../../examples/providers/factory.py
   :language: python

Factory providers and injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Objects can take dependencies in different forms. Some objects take init
arguments, other are using attributes setting or method calls to be
initialized. It affects how such objects need to be created and initialized,
and that is the place where ``dependency_injector.injections`` need to be used.

``Factory`` provider takes various number of positional arguments, that define
what kind of dependency injections need to be done.

All of those instructions are defined in ``dependency_injector.injections`` 
module and are subclasses of ``dependency_injector.injections.Injection``. 
There  are several types of injections that are used by ``Factory`` provider:

+ ``KwArg`` - injection is done by passing injectable value in object's
  ``__init__()`` method in time of object's creation via keyword argument.
  Takes keyword name of ``__init__()`` argument and injectable value.
+ ``Attribute`` - injection is done by setting specified attribute with
  injectable value right after object's creation. Takes attribute's name
  and injectable value.
+ ``Method`` - injection is done by calling of specified method with
  injectable value right after object's creation and attribute injections
  are done. Takes method name and injectable value.

All ``Injection``'s injectable values are provided *"as is"*, except of
providers. Providers will be called every time, when injection needs to be
done.


Factory providers and __init__ injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example below shows how to create ``Factory`` of particular class with
``__init__`` keyword argument injections which injectable values are also
provided by another factories:

.. image:: /images/providers/factory_init_injections.png
    :width: 90%
    :align: center

.. literalinclude:: ../../examples/providers/factory_init_injections.py
   :language: python

Next example shows how ``Factory`` provider deals with positional and keyword
``__init__`` context arguments. In few words, ``Factory`` provider fully
passes positional context arguments to class's ``__init__`` method, but
keyword context arguments have priority on ``KwArg`` injections (this could be
useful for testing).

So, please, follow the example below:

.. image:: /images/providers/factory_init_injections_and_contexts.png

.. literalinclude:: ../../examples/providers/factory_init_injections_and_contexts.py
   :language: python

Factory providers and attribute injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example below shows how to create ``Factory`` of particular class with
attribute injections. Those injections are done by setting specified attributes
with injectable values right after object's creation.

Example:

.. image:: /images/providers/factory_attribute_injections.png

.. literalinclude:: ../../examples/providers/factory_attribute_injections.py
   :language: python

Factory providers and method injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Current example shows how to create ``di.Factory`` of particular class with
method injections. Those injections are done by calling of specified method
with injectable value right after object's creation and attribute injections
are done.

Method injections are not very popular in Python due Python best practices
(usage of public attributes instead of setter methods), but they may appear in
some cases.

Example:

.. image:: /images/providers/factory_method_injections.png

.. literalinclude:: ../../examples/providers/factory_method_injections.py
   :language: python

Factory providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``di.Factory`` provider could be delegated to any other provider via any kind 
of injection. As it was mentioned earlier, if ``di.Factory`` is injectable 
value, it will be called every time when injection is done. ``di.Factory`` 
delegation is performed by wrapping delegated ``di.Factory`` into special 
provider type - ``di.Delegate``, that just returns wrapped ``di.Factory``. 
Saying in other words, delegation of factories - is a way to inject factories 
themselves, instead of results of their calls. 


Actually, there are two ways of creating factory delegates:

+ ``di.Delegate(di.Factory(...))`` - obviously wrapping factory into 
  ``di.Delegate`` provider.
+ ``di.Factory(...).delegate()`` - calling factory ``delegate()`` method, that 
  returns delegate wrapper for current factory.

Example:

.. image:: /images/providers/factory_delegation.png
    :width: 85%
    :align: center

.. literalinclude:: ../../examples/providers/factory_delegation.py
   :language: python
