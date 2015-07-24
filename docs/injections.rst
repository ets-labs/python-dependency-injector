Injections
==========

Injections are *Objects* entities that are used for specification of dependency
injection types.

Different functions, classes and objects can take dependency injections in
various forms. Some of them take dependencies like keyword arguments during
call time, other require setting of attributes or calling of specialized
methods for doing dependency injections.

So, when you are doing dependency injection you need to specify its type and
that is the place where *Injections* need to be used.

Some key points of *Objects* injections:

    - Every *Objects* injection always takes injectable value as an
      ``injectable`` param. Every Python object could be an injectable.
    - Every *Objects* injection always has ``value`` property that returns
      injection's injectable. ``value`` property is calculated every time it is
      accessed. Every Python object, except of *Objects* providers, that was
      provided as and ``injectable`` will be returned by ``value`` property
      *"as is"*. *Objects* providers will be called every time during ``value``
      accessing and result of such calls will be returned.
    - Every *Objects* *Injection* can have additional params that are needed
      for doing particular type of injection.

There are several types of *Injections*:

    - ``KwArg`` - is used for making keyword argument injections for any kind
      of callables (functions, methods, objects instantiation and so on). Takes
      keyword argument name as string and injectable.
    - ``Attribute`` - is used for making injections by setting of injection's
      value to a particular attribute. Takes attribute name as string and
      injectable.
    - ``Method`` - is used for making injections by calling of method with
      injectable value. Takes method name as string and injectable.
