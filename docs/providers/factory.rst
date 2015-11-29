Factory providers
-----------------

.. currentmodule:: dependency_injector.providers

:py:class:`Factory` provider creates new instance of specified class on every 
call.

Nothing could be better than brief example:

.. image:: /images/providers/factory.png
    :width: 80%
    :align: center

.. literalinclude:: ../../examples/providers/factory.py
   :language: python

Factory providers and __init__ injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Factory` takes a various number of positional and keyword arguments 
that are used as ``__init__()`` injections. Every time, when 
:py:class:`Factory` creates new one instance, positional and keyword 
argument injections would be passed as an instance's arguments.

Such behaviour is very similar to the standard Python ``functools.partial`` 
object, except of one thing: all injectable values are provided 
*"as is"*, except of providers (subclasses of :py:class:`Provider`). Providers 
will be called every time, when injection needs to be done. For example, 
if injectable value of injection is a :py:class:`Factory`, it will provide 
new one instance (as a result of its call) every time, when injection needs 
to be done.

Example below is a little bit more complicated. It shows how to create 
:py:class:`Factory` of particular class with ``__init__()`` argument 
injections which injectable values are also provided by another factories:

.. note:: 

    Current positional and keyword argument injections syntax (in the examples
    below) is a **simplified one** version of full syntax. Examples of full 
    syntax and other types of injections could be found in sections below.

    While positional / keyword argument injections may be the best way of 
    passing injections, current simplified syntax might be the preferable one 
    and could be widely used.

.. image:: /images/providers/factory_init_injections.png
    :width: 90%
    :align: center

Example of usage positional argument injections:

.. literalinclude:: ../../examples/providers/factory_init_args.py
   :language: python

Example of usage keyword argument injections:

.. literalinclude:: ../../examples/providers/factory_init_kwargs.py
   :language: python

Factory providers and __init__ injections priority
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next example shows how :py:class:`Factory` provider deals with positional and 
keyword ``__init__()`` context arguments. In few words, :py:class:`Factory` 
behaviour here is very like a standard Python ``functools.partial``:

- Positional context arguments will be appended after :py:class:`Factory` 
  positional injections.
- Keyword context arguments have priority on :py:class:`Factory` keyword 
  injections and will be merged over them.

So, please, follow the example below:

.. image:: /images/providers/factory_init_injections_and_contexts.png

.. literalinclude:: ../../examples/providers/factory_init_injections_and_contexts.py
   :language: python


Factory providers and other types of injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Objects can take dependencies in different forms (some objects take init
arguments, other use attributes setting or method calls). It affects how 
such objects are created and initialized.

:py:class:`Factory` provider takes various number of positional and keyword 
arguments, that define what kinds of dependency injections have to be used.

All of those instructions are defined in 
:py:mod:`dependency_injector.injections` module and are subclasses of 
:py:class:`dependency_injector.injections.Injection`. There are several types 
of injections that are used by :py:class:`Factory` provider:

+ :py:class:`dependency_injector.injections.Arg` - injection is done by 
  passing injectable value in object's ``__init__()`` method in time of 
  object's creation as positional argument. Takes injectable value only.
+ :py:class:`dependency_injector.injections.KwArg` - injection is done by 
  passing injectable value in object's ``__init__()`` method in time of 
  object's creation as keyword argument.  Takes keyword name of 
  ``__init__()`` argument and injectable value.
+ :py:class:`dependency_injector.injections.Attribute` - injection is done 
  by setting specified attribute with injectable value right after 
  object's creation. Takes attribute's name and injectable value.
+ :py:class:`dependency_injector.injections.Method` - injection is done by 
  calling of specified method with injectable value right after object's 
  creation and attribute injections are done. Takes method name and 
  injectable value.

All :py:class:`dependency_injector.injections.Injection`'s injectable values 
are provided *"as is"*, except of providers (subclasses of 
:py:class:`Provider`). Providers will be called every time, when injection 
needs to be done.

Factory providers and attribute injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example below shows how to create :py:class:`Factory` of particular class with
attribute injections. Those injections are done by setting specified attributes
with injectable values right after object's creation.

Example:

.. image:: /images/providers/factory_attribute_injections.png

.. literalinclude:: ../../examples/providers/factory_attribute_injections.py
   :language: python

Factory providers and method injections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Current example shows how to create :py:class:`Factory` of particular class
with method injections. Those injections are done by calling of specified 
method with injectable value right after object's creation and attribute 
injections are done.

Method injections are not very popular in Python due Python best practices
(usage of public attributes instead of setter methods), but they may appear in
some cases.

Example:

.. image:: /images/providers/factory_method_injections.png

.. literalinclude:: ../../examples/providers/factory_method_injections.py
   :language: python

Factory providers delegation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Factory` provider could be delegated to any other provider via any 
kind of injection. As it was mentioned earlier, if :py:class:`Factory` is 
injectable value, it will be called every time when injection is done. 
:py:class:`Factory` delegation is performed by wrapping delegated 
:py:class:`Factory` into special provider type - :py:class:`Delegate`, that 
just returns wrapped :py:class:`Factory`. Saying in other words, delegation 
of factories - is a way to inject factories themselves, instead of results 
of their calls. 

Actually, there are two ways of creating factory delegates:

+ ``Delegate(Factory(...))`` - obviously wrapping factory into 
  :py:class:`Delegate` provider.
+ ``Factory(...).delegate()`` - calling factory :py:meth:`Factory.delegate` 
  method, that returns delegate wrapper for current factory.

Example:

.. image:: /images/providers/factory_delegation.png
    :width: 85%
    :align: center

.. literalinclude:: ../../examples/providers/factory_delegation.py
   :language: python
