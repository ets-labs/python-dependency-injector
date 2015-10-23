Changelog
=========

This document describes all the changes in *Dependency Injector* framework 
that were made in every particular version.

From version 0.7.6 *Dependency Injector* framework strictly 
follows `Semantic versioning`_


Development version
-------------------

- Add functionality for creating ``di.AbstractCatalog`` provider bundles.
- Improve ``di.AbstractCatalog`` inheritance.
- Improve ``di.AbstractCatalog`` overriding.
- Add images for catalog "Writing catalogs" and "Operating with catalogs" 
  examples.
- Add functionality for using positional argument injections with 
  ``di.Factory``, ``di.Singleton``, ``di.Callable`` providers and 
  ``di.inject`` decorator.
- Add functionality for decorating classes with ``@di.inject``.
- Add ``di.Singleton.injections`` attribute that represents a tuple of all 
  ``di.Singleton`` injections (including args, kwargs, attributes and methods).
- Add ``di.Callable.injections`` attribute that represents a tuple of all 
  ``di.Callable`` injections (including args and kwargs).
- Add optimization for ``di.Injection.value`` property that will compute 
  type of injection once, instead of doing this on every call.
- Add ``di.VERSION`` constant for verification of currently installed version.
- Add support of Python 3.5.
- Add support of six 1.10.0.
- Add minor refactorings and code style fixes.

0.9.5
-----
- Change provider attributes scope to public.
- Add ``di.Factory.injections`` attribute that represents a tuple of all 
  ``di.Factory`` injections (including kwargs, attributes and methods).

0.9.4
-----
- Add minor documentation fixes.

0.9.3
-----
- Implement thread safety.

0.9.2
-----
- Add minor refactorings.

0.9.1
-----
- Add simplified syntax of kwarg injections for ``di.Factory`` and 
  ``di.Singleton`` providers: 
  ``di.Factory(SomeClass, dependency1=injectable_provider_or_value)``.
- Add simplified syntax of kwarg injections for ``di.Callable`` provider:
  ``di.Callable(some_callable, dependency1=injectable_provider_or_value)``
- Add simplified syntax of kwarg injections for ``@di.inject`` decorator:
  ``@di.inject(dependency1=injectable_provider_or_value)``.
- Optimize ``@di.inject()`` decorations when they were made several times for 
  the same callback.
- Add minor refactorings.
- Fix of minor documentation issues.

0.8.1
-----
- ``Objects`` is renamed to ``Dependency Injector``.

0.7.8
-----
- Fixing @inject import bug in examples.

0.7.7
-----
- Fixing minor bug in concept example.

0.7.6
-----

- Adding support of six from 1.7.0 to 1.9.0. 
- Factory / Singleton providers are free from restriction to operate with 
  classes only. This feature gives a change to use factory method and 
  functions with Factory / Singleton providers.
- All attributes of all entities that have to be protected was renamed using 
  ``_protected`` manner. 
- Providers extending was improved by implementing overriding logic in 
  ``Provider.__call__()`` and moving providing logic into 
  ``Provider._provide()``.
- ``NewInstance`` provider was renamed to ``Factory`` provider. 
  ``NewInstance`` still can be used, but it considered to be deprecated and 
  will be removed in futher releases.
- ``@inject`` decorator was refactored to keep all injections in 
  ``_injections`` attribute of decorated callback. It will give a possibilty to
  track all the injections of particular callbacks and gives some performance 
  boost due minimizing number of calls for doing injections.
- A lot of documentation updates were made.
- A lot of examples were added.
- Some minor refactorings were done.

Previous versions
-----------------

- While *Objects* was in alpha state, changes were not tracked.

.. _Semantic versioning: http://semver.org/
