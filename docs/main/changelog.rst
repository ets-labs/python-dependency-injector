Changelog
=========

This document describes all the changes in *Dependency Injector* framework 
that were made in every particular version.

From version 0.7.6 *Dependency Injector* framework strictly 
follows `Semantic versioning`_

Development version
-------------------
- Add ``Coroutine`` provider.
- Add ``DelegatedCoroutine`` provider.
- Add ``AbstractCoroutine`` provider.
- Add ``CoroutineDelegate`` provider.
- Regenerate C sources using Cython 0.28.5.

3.13.2
------
- Add additional benchmark of ``Factory`` provider.
- Add tests and tox.ini to the distribution, so that they could be used after
  package is installed (thanks to
  `Tobias Happ <https://github.com/Gerschtli>`_).

3.13.1
------
- Fix typo on "Chained Factories" pattern docs page.

3.13.0
------
- Add Python 3.7 support.
- Drop Python 3.3 support.
- Drop Python 2.6 support.
- Add example of "Chained Factories" pattern.
- Add example of "Factory of Factories" pattern.

3.12.4
------
- Fix bug `#200 <https://github.com/ets-labs/python-dependency-injector/issues/200>`_.
- Make some refactoring `#199 <https://github.com/ets-labs/python-dependency-injector/issues/199>`_.

3.12.3
------
- Fix bug `#198 <https://github.com/ets-labs/python-dependency-injector/issues/198>`_.
- Regenerate C sources using Cython 0.28.4.

3.12.2
------
- Apply code style fixes to "services_v2" example miniapp.

3.12.1
------
- Update main page example from "services_v1" to "services_v2".
- Fix few typos on main page.
- Add new example miniapp "password_hashing".
- Add new example miniapp "services_v2".
- Rename example miniapp "services" to "services_v1".
- Fix incompatibility issue between Python 3.3, pip 10.0.0 and virtualenv
  16.0.0 (`details <https://github.com/awslabs/base64io-python/issues/4>`_)
  that caused failures of Python 3.3 tests on Travis.
- Regenerate C sources using Cython 0.28.3.

3.12.0
------
- Regenerate C sources using Cython 0.28.2.

3.11.3
------
- Fix padding problem in code samples in docs.

3.11.2
------
- Fix padding problem in code samples in docs.
- Remove ``autodoc`` from the list of documentation dependencies.

3.11.1
------
- Fix small typo in documentation (thanks to James Lafa).

3.11.0
------
- Improve ``Configuration`` provider overriding logic.
- Refactor ``Configuration`` provider.
- Improve ``DependenciesContainer`` provider overriding logic.
- Update "services" example miniapp.
- Update "bundles" example miniapp.

3.10.0
------
- Add ``DependenciesContainer`` provider.
- Add "use_cases" example miniapp.
- Update documentation requirements to use fixed version of 
  ``sphinxcontrib-disqus``.


3.9.1
-----
- Fix docs build problem (``sphinx`` is frozen on ``1.5.6`` version because of
  incompatibility with ``sphinxcontrib-discus``). 
- Add badge for docs.

3.9.0
-----
- Change initialization of declarative container, so it accepts overriding 
  providers as keyword arguments - 
  ``DeclarativeContainer(**overriding_providers)``.
- Add method to dynamic catalog for setting groups of providers -  
  ``DynamicContainer.set_providers(**providers)``.
- Add method to dynamic catalog for overriding groups of providers -  
  ``DynamicContainer.set_providers(**overriding_providers)``.
- Rename ``ExternalDependency`` provider to ``Dependency``.
- Add default value for ``instance_of`` argument of ``Dependency`` provider -
  ``Dependency(instance_of=object)``.
- Fix bug when copying ``Configuration`` provider.
- Regenerate C sources using Cython 0.27.3.
- Add "bundles" example miniapp.


3.8.2
-----
- Fix padding problem in code samples in docs (part 2).

3.8.1
-----
- Fix padding problem in code samples in docs.

3.8.0
-----
- Add ``DeclarativeContainer.containers`` attribute that stores dictionary of
  nested containers.
- Fix bug related to double-overridden providers (provider1 -> provider2 ->
  provider3).

3.7.1
-----
- Add support of six 1.11.0.

3.7.0
-----
- Add ``FactoryAggregate`` provider.
- Add ``Provider.provider`` dynamic attribute that return new provider's 
  delegate (alias of method ``Provider.delegate()``).
- Add support of six 1.11.0.
- Regenerate C sources using Cython 0.27.1.

3.6.1
-----
- Regenerate C sources using Cython 0.26.

3.6.0
-----
- Add ``CallableDelegate`` provider.
- Add ``FactoryDelegate`` provider.
- Add ``SingletonDelegate`` provider.

3.5.0
-----
- Add functionality for initializing ``Configuration`` provider with default 
  values.

3.4.8
-----
- Code style fixes in ``providers`` module.

3.4.7
-----
- Correct typo in changelog.

3.4.6
-----
- Add "Useful links" section to the "Dependency injection and inversion of
  control in Python" article.

3.4.5
-----
- Remove non-ascii character from README. This character created an
  installation problem on Debian (Python 3.4).

3.4.4
-----
- Add ``Provider.last_overriding`` read-only property that points to last 
  overriding provider, if any. If target provider is not overridden, ``None``
  would be returned.
- Update example of writing custom providers.
- Update movie lister example miniapp.
- Update source of ``coveralls.io`` badge.

3.4.3
-----
- Update doc block for ``Provider.overriding_lock`` attribute.

3.4.2
-----
- Make ``Provider`` overriding methods thread safe:
  ``Provider.override(provider)``, ``Provider.reset_last_overriding()``, 
  ``Provider.reset_override()``.
- Refactor storage locking of ``ThreadSafeSingleton`` provider.
- Fix few ``pydocstyle`` errors in examples.

3.4.1
-----
- Update movie lister example miniapp with ``AbstractFactory`` provider.

3.4.0
-----
- Add ``AbstractCallable`` provider.
- Add ``AbstractFactory`` provider.
- Add ``AbstractSingleton`` provider.
- Optimize calling of overridden providers (~15% faster).

3.3.7
-----
- Fix minor bug related to patch of ``Configuration`` provider in version
  3.3.6 - special attribues were identified by formula ``__{text}`` - now
  they are identified by formula ``__{text}__``, that is more correct
  according to Python Data Model.

3.3.6
-----
- Patch ``Configuration`` provider to raise ``AttributeError`` when there
  is an attempt to access special attribute like ``__module__`` or
  ``__name__`` (this behaviour is identical to behaviour of ``object``).
- Apply minor refactoring for ``providers`` module.
- Remove cythonization from travis building process.

3.3.5
-----
- [Refactoring] Consolidate all containers in
  ``dependency_injector.containers`` module.
- [Refactoring] Consolidate all providers in
  ``dependency_injector.providers`` module.

3.3.4
-----
- Change ``__module__`` attribute for all members of
  ``dependency_injector.containers`` package to point to package, but not to
  package modules.
- Regenerate C sources using Cython 0.25.2.

3.3.3
-----
- Update services miniapp example.

3.3.2
-----
- Add `disqus.com <https://disqus.com/>`_ comments for documentation.
- Fix reference to version in api docs.
- Fix title underline in containers api docs.
- Update documentation copyright year.
- Update example version in installation document.

3.3.1
-----
- Add some improvements to the documentation.

3.3.0
-----
- Add support of Python 3.6.

3.2.5
-----
- Add description of structure into README.
- Fix documentation errors.

3.2.4
-----
- Switch to single version of documentation for getting shorter urls (without 
  ``/en/stable/``). Add appropriate redirects for compatibility with previous 
  links.
- Update copyright date.

3.2.3
-----
- Add examples into README.
- Make minor documentation updates.

3.2.2
-----
- Change name of version variable to follow PEP8: ``VERSION`` -> ``__version__``.

3.2.1
-----
- Update ``services`` miniapp example.

3.2.0
-----
- Add ``Configuration`` provider for late static binding of configuration 
  options.

3.1.5
-----
- Refactor provider internals: C functions naming scheme and code layout.
- Add Terrence Brannon (metaperl) to the list of contributors.

3.1.4
-----
- Move ``inline`` functions from class level to module level for removing them 
  from virtual table and enable inlining.

3.1.3
-----
- Fix flake8 ``E305`` error in examples.

3.1.2
-----
- Remove ``public`` (``extern``) modifier utils constants.
- Fix flake8 ``E305`` error in examples.

3.1.1
-----
- Fix minor typo in README.

3.1.0
-----
- Add "Services mini application" example.
- Fix minor error in ``Factory`` provider API doc.

3.0.1
-----
- Add ``*.c`` source files under version control.
- Change keywords.


3.0.0
-----

- **Providers**

  1. All providers from ``dependency_injector.providers`` package are 
     implemented as C extension types using Cython.
  2. Add ``BaseSingleton`` super class for all singleton providers.
  3. Make ``Singleton`` provider not thread-safe. It makes performance of 
     ``Singleton`` provider  10x times faster.
  4. Add ``ThreadSafeSingleton`` provider - thread-safe version of 
     ``Singleton`` provider.
  5. Add ``ThreadLocalSingleton`` provider - ``Singleton`` provider that uses 
     thread-local storage.
  6. Remove ``provides`` attribute from ``Factory`` and ``Singleton`` 
     providers.
  7. Add ``set_args()`` and ``clear_args()`` methods for ``Callable``, 
     ``Factory`` and ``Singleton`` providers.

- **Containers**

  1. Module ``dependency_injector.containers`` was splitted into submodules 
     without any functional changes.

- **Utils**

  1. Module ``dependency_injector.utils`` is splitted into 
     ``dependency_injector.containers`` and ``dependency_injector.providers``.

- **Miscellaneous**

  1. Remove ``@inject`` decorator.
  2. Add makefile (``clean``, ``test``, ``build``, ``install``, ``uninstall`` 
     & ``publish`` commands).
  3. Update repository structure:
    1. Sources are moved under ``src/`` folder.
    2. Tests are moved under ``tests/unit/`` folder.


2.2.10
------
- Fix typo in README.

2.2.9
-----
- Add github badges to readme and docs index pages.
- Update service names in services example miniapp.
- Create engines & cars example miniapp.

2.2.8
-----
- Move fixtures to separate module in movie lister example.

2.2.7
-----
- Fix typo in README.

2.2.6
-----
- Update README.
- Update docs index page.

2.2.5
-----
- Fix typo in README.

2.2.4
-----
- Update README.

2.2.3
-----
- Update README.

2.2.2
-----
- Update README.

2.2.1
-----
- Update examples.

2.2.0
-----
- Deprecate ``inject`` decorator.

2.1.1
-----
- Normalize package names by PEP-503.

2.1.0
-----
- Add ``ThreadLocalSingleton`` and ``DelegatedThreadLocalSingleton`` providers.
- Add documentation section about singleton providers and multi-threading.
- Update API docs of creational providers.

2.0.0
------
- Introduce new injections style for ``Callable``, ``Factory`` & 
  ``Singleton`` providers.
- Drop providers: ``Static``, ``Value``, ``Function``, ``Class``, ``Config``.
- Increase performance of making injections in 2 times (+100%).
- Drop method injections.
- Simplify providers overriding system.
- Replace ``catalogs`` package with ``containers`` module.
- Drop all backward compatibilities for 1.x.
- Refactor most of the components.
- Update documentation.

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

.. disqus::


.. _Semantic versioning: http://semver.org/
