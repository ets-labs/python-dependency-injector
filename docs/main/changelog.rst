Changelog
=========

This document describes all the changes in *Dependency Injector* framework 
that were made in every particular version.

From version 0.7.6 *Dependency Injector* framework strictly 
follows `Semantic versioning`_

Development version
-------------------
- No features.

2.0.0
------
- Drop backward compatibilities of 1.x.
- Drop providers:
  - ``Static``
  - ``Value``
  - ``Function``
  - ``Class``
  - ``Config``
- Drop ``Method`` injections.

1.17.0
------
- Add ``add_injections()`` method to ``Callable``, ``DelegatedCallable``, 
  ``Factory``, ``DelegatedFactory``, ``Singleton`` and ``DelegatedSingleton`` 
  providers.
- Fix bug with accessing to declarative catalog attributes from instance level.

1.16.8
------
- Fix some typos in introduction section of documentation.

1.16.7
------
- Add some changes into introduction section of documentation.

1.16.5
------
- Move project to ``https://github.com/ets-labs/python-dependency-injector``.
- Move project docs to ``http://python-dependency-injector.ets-labs.org/``.

1.16.4
------
- Add some documentation improvements.

1.16.1
------
- Add ``@copy`` decorator for copying declarative catalog providers.
- Add line numbers for all code samples in documentation.
- Add "Examples" section into documentation.
- Add "Movie Lister" example.
- Add "Services" example.
- Move project documentation into organisation's domain 
  (dependency-injector.ets-labs.org).

1.15.2
------
- [Refactoring] split ``catalogs`` module into smaller modules, 
  ``catalogs`` module become a package.
- [Refactoring] split ``providers`` module into smaller modules, 
  ``providers`` module  become a package.
- Update introduction documentation.

1.15.1
------
- Update package information and documentation.

1.15.0
------
- Add ``Provider.provide()`` method. ``Provider.__call__()`` become a 
  reference to ``Provider.provide()``.
- Add provider overriding context.
- Update main examples and README.

1.14.11
-------
- Update README.

1.14.10
-------
- Add "catalog-providing-callbacks" example and several tests for it.

1.14.9
------
- Add ``override`` decorator in providers module.
- Add storing of originally decorated instance in ``inject`` decorator.
- Add several refactorings.
- Switch to ``pydocstyle`` tool from ``pep257``.

1.14.8
------
- Update README.

1.14.7
------
- Add one more example in README (inline providers and injections).

1.14.6
------
- Add ``cls`` alias for ``provides`` attributes of ``Factory``, 
  ``DelegatedFactory``, ``Singleton`` and ``DelegatedSingleton`` providers.

1.14.5
------
- Fix typo in provider's error message.

1.14.4
------
- Update documentation.

1.14.3
------
- Optimize internals of providers.
- Optimize ``Callable`` provider.
- Optimize ``Factory`` provider.
- Optimize ``Singleton`` provider.

1.14.2
------
- Update documentation and description.

1.14.1
------
- Add meta description & keywords on docs index page.

1.14.0
------
- Drop support of Python 3.2.

1.13.2
------
- Update PyPi info.

1.13.1
------
- Transfer ownership to `ETS Labs <https://github.com/ets-labs>`_.

1.13.0
------
- Add ``DelegatedCallable`` provider.
- Add ``DelegatedFactory`` provider.
- Add ``DelegatedSingleton`` provider.
- Add some documentation improvements.

1.12.0
------
- Add possibility to specialize ``Factory`` provided type.
- Add possibility to specialize ``Singleton`` provided type.
- Add possibility to specialize ``DeclarativeCatalog`` provider type.
- Add possibility to specialize ``DynamicCatalog`` provider type.
- Make some refactorings for providers.

1.11.2
------
- Improve representation of providers and injections.

1.11.1
------
Previous state of *Dependency Injector* framework (0.11.0 version) is 
considered to be production ready / stable, so current release is considered 
to be the first major release.

- Increase major version. 
- Backward compatibility with all previous versions above 0.7.6 has been saved.

0.11.0
------
- Rename ``AbstractCatalog`` to ``DeclarativeCatalog`` 
  (with backward compatibility).
- Rename ``catalog`` module to ``catalogs`` with backward compatibility.
- Implement dynamic binding of providers for ``DeclarativeCatalog``.
- Add ``DynamicCatalog``.
- Change restrictions for providers-to-catalogs bindings - provider could be 
  bound to several catalogs with different names.
- Restrict overriding of providers by themselves.
- Restrict overriding of catalogs by themselves.
- Make ``DeclarativeCatalog.last_overriding`` attribute to be ``None`` by 
  default.
- Make ``Provider.last_overriding`` attribute to be ``None`` by 
  default.
- Refactor catalogs and providers modules.
- Add API documentation
- Improve user's guides and examples.

0.10.5
------
- Add more representable implementation for ``AbstractCatalog`` and 
  ``AbstractCatalog.Bundle``.

0.10.4
------
- Remove VERSION file from MANIFEST.in.

0.10.3
------
- Update example docblocks.

0.10.2
------
- Fix bug with injecting entities that implement ``__getattr__``.

0.10.1
------
- Update some examples.

0.10.0
------
- Add functionality for creating ``AbstractCatalog`` provider bundles.
- Improve ``AbstractCatalog`` inheritance.
- Improve ``AbstractCatalog`` overriding.
- Add images for catalog "Writing catalogs" and "Operating with catalogs" 
  examples.
- Add functionality for using positional argument injections with 
  ``Factory``, ``Singleton``, ``Callable`` providers and 
  ``inject`` decorator.
- Add functionality for decorating classes with ``@inject``.
- Add ``Singleton.injections`` attribute that represents a tuple of all 
  ``Singleton`` injections (including args, kwargs, attributes and methods).
- Add ``Callable.injections`` attribute that represents a tuple of all 
  ``Callable`` injections (including args and kwargs).
- Add optimization for ``Injection.value`` property that will compute 
  type of injection once, instead of doing this on every call.
- Add ``VERSION`` constant for verification of currently installed version.
- Add support of Python 3.5.
- Add support of six 1.10.0.
- Add minor refactorings and code style fixes.

0.9.5
-----
- Change provider attributes scope to public.
- Add ``Factory.injections`` attribute that represents a tuple of all 
  ``Factory`` injections (including kwargs, attributes and methods).

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
