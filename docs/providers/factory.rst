Factory providers
-----------------

``di.Factory`` provider creates new instance of specified class on every call.

Nothing could be better than brief example:

.. image:: /images/providers/factory.png
    :width: 80%
    :align: center

.. literalinclude:: ../../examples/providers/factory.py
   :language: python

Factory providers and __init__ injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``di.Factory`` takes a various number of keyword arguments that are 
transformed into keyword argument injections. Every time, when ``di.Factory`` 
creates new one instance, keyword argument injections would be passed as an
instance's keyword arguments. 

All injectable values are provided *"as is"*, except of providers (subclasses 
of ``di.Provider``). Providers will be called every time, when injection needs 
to be done. For example, if injectable value of keyword argument injection is a
``di.Factory``, it will provide new one instance (as a result of its call) as 
an injectable value every time, when injection needs to be done.

Example below is a little bit more complicated. It shows how to create 
``di.Factory`` of particular class with ``__init__`` keyword argument 
injections which injectable values are also provided by another factories:

.. note:: 

    Current keyword argument injections syntax (in an example below) is a 
    **simplified one**. Full syntax and other types of injections could be 
    found in sections below.

    While keyword argument injections may be the best way of passing 
    injections, current simplified syntax might be the preferable one and 
    could be widely used.

.. image:: /images/providers/factory_init_injections.png
    :width: 90%
    :align: center

.. literalinclude:: ../../examples/providers/factory_init_injections.py
   :language: python

Factory providers and __init__ injections priority
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next example shows how ``di.Factory`` provider deals with positional and 
keyword ``__init__`` context arguments. In few words, ``di.Factory`` 
provider fully passes positional context arguments to class's ``__init__`` 
method, but keyword context arguments have priority on predefined keyword 
argument injections.

So, please, follow the example below:

.. image:: /images/providers/factory_init_injections_and_contexts.png

.. literalinclude:: ../../examples/providers/factory_init_injections_and_contexts.py
   :language: python


Factory providers and other types of injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Objects can take dependencies in different forms(some objects take init
arguments, other use attributes setting or method calls). It affects how 
such objects are created and initialized.

``di.Factory`` provider takes various number of positional and keyword 
arguments, that define what kinds of dependency injections have to be used.

All of those instructions are defined in ``di.injections`` module and are 
subclasses of ``di.injections.Injection`` (shortcut ``di.Injection``). There 
are several types of injections that are used by ``di.Factory`` provider:

+ ``di.KwArg`` - injection is done by passing injectable value in object's
  ``__init__()`` method in time of object's creation via keyword argument.
  Takes keyword name of ``__init__()`` argument and injectable value.
+ ``di.Attribute`` - injection is done by setting specified attribute with
  injectable value right after object's creation. Takes attribute's name
  and injectable value.
+ ``di.Method`` - injection is done by calling of specified method with
  injectable value right after object's creation and attribute injections
  are done. Takes method name and injectable value.

All ``di.Injection``'s injectable values are provided *"as is"*, except of
providers (subclasses of ``di.Provider``). Providers will be called every time,
when injection needs to be done.

Factory providers and attribute injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example below shows how to create ``di.Factory`` of particular class with
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
