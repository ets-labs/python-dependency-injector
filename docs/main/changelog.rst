Changelog
=========

This document describes all the changes in *Dependency Injector* framework
that were made in every particular version.

From version 0.7.6 *Dependency Injector* framework strictly
follows `Semantic versioning`_

Develop
-------

- Drop support of Python 2.7, 3.5, and 3.6.
- Regenerate C sources using Cython 0.29.36.

4.41.0
------
- Add support of Python 3.11.
- Allow Closing to detect dependent resources `#633 <https://github.com/ets-labs/python-dependency-injector/issues/633>`_,
  `#636 <https://github.com/ets-labs/python-dependency-injector/pull/636>`_. Thanks `Jamie Stumme @StummeJ <https://github.com/StummeJ>`_
  for the contribution.
- Update CI/CD to use Ubuntu 22.04.
- Update CI/CD to ``actions/checkout@v3``, ``actions/setup-python@v4``, ``actions/upload-artifact@v3``, ``pypa/cibuildwheel@v2.11.3``,
  and ``actions/download-artifact@v3``.
- Fix install crash on non-utf8 systems `#644 <https://github.com/ets-labs/python-dependency-injector/pull/644>`_.
- Fix a bug in Windows build with default charset `#635 <https://github.com/ets-labs/python-dependency-injector/pull/635>`_.
- Update FastAPI Redis example to use ``aioredis`` version 2 `#613 <https://github.com/ets-labs/python-dependency-injector/pull/613>`_.
- Update documentation on creating custom providers `#598 <https://github.com/ets-labs/python-dependency-injector/pull/598>`_.
- Regenerate C sources using Cython 0.29.32.
- Fix builds badge.

4.40.0
------
- Add ``Configuration.from_json()`` method to load configuration from a json file.
- Fix bug with wiring not working properly with functions double wrapped by ``@functools.wraps`` decorator.
  See issue: `#454 <https://github.com/ets-labs/python-dependency-injector/issues/454>`_.
  Many thanks to: `@platipo <https://github.com/platipo>`_, `@MatthieuMoreau0 <https://github.com/MatthieuMoreau0>`_,
  `@fabiocerqueira <https://github.com/fabiocerqueira>`_, `@Jitesh-Khuttan <https://github.com/Jitesh-Khuttan>`_.
- Refactor wiring module to store all patched callable data in the ``PatchedRegistry``.
- Improve wording on the "Dependency injection and inversion of control in Python" docs page.
- Add documentation on the ``@inject`` decorator.
- Update typing in the main example and cohesion/coupling correlation definition in
  "Dependency injection and inversion of control in Python".
  Thanks to `@illia-v (Illia Volochii) <https://github.com/illia-v>`_ for the
  PR (`#580 <https://github.com/ets-labs/python-dependency-injector/pull/580>`_).
- Update copyright year.
- Enable skipped test ``test_schema_with_boto3_session()``.
- Update pytest configuration.
- Regenerate C sources using Cython 0.29.30.

4.39.1
------
- Fix bug `#574 <https://github.com/ets-labs/python-dependency-injector/issues/574>`_:
  "``@inject`` breaks ``inspect.iscoroutinefunction``". Thanks to
  `@burritoatspoton (Rafał Burczyński) <https://github.com/burritoatspoton>`_ for reporting the issue.

4.39.0
------
- Optimize injections and wiring from x1.5 to x7 times depending on the use case.
- Fix bug `#569 <https://github.com/ets-labs/python-dependency-injector/issues/569>`_:
  "numpy.typing.NDArray breaks wiring". Thanks to
  `@VKFisher (Vlad Fisher) <https://github.com/VKFisher>`_ for reporting the issue and providing a fix.

4.38.0
------
- Add new provider ``Aggregate``. It is a generalized version of ``FactoryAggregate`` that
  can contain providers of any type, not only ``Factory``. See issue
  `#530 <https://github.com/ets-labs/python-dependency-injector/issues/530>`_. Thanks to
  `@zerlok (Danil Troshnev) <https://github.com/zerlok>`_ for suggesting the feature.
- Add argument ``as_`` to the ``config.from_env()`` method for the explicit type casting
  of an environment variable value, e.g.: ``config.timeout.from_env("TIMEOUT", as_=int)``.
  See issue `#533 <https://github.com/ets-labs/python-dependency-injector/issues/533>`_. Thanks to
  `@gtors (Andrey Torsunov) <https://github.com/gtors>`_ for suggesting the feature.
- Add ``.providers`` attribute to the ``FactoryAggregate`` provider. It is an alias for
  ``FactoryAggregate.factories`` attribute.
- Add ``.set_providers()`` method to the ``FactoryAggregate`` provider. It is an alias for
  ``FactoryAggregate.set_factories()`` method.
- Add string imports for ``Factory``, ``Singleton``, ``Callable``, ``Resource``, and ``Coroutine``
  providers, e.g. ``Factory("module.Class")``.
  See issue `#531 <https://github.com/ets-labs/python-dependency-injector/issues/531>`_.
  Thanks to `@al-stefanitsky-mozdor <https://github.com/al-stefanitsky-mozdor>`_ for suggesting the feature.
- Fix ``Dependency`` provider to don't raise "Dependency is not defined" error when the ``default``
  is a falsy value of proper type.
  See issue `#550 <https://github.com/ets-labs/python-dependency-injector/issues/550>`_. Thanks to
  `@approxit <https://github.com/approxit>`_ for reporting the issue.
- Refactor ``FactoryAggregate`` provider internals.
- Update logo on Github and in docs to support dark themes and remove some imperfections.

4.37.0
------
- Add support of Python 3.10.
- Improve wiring with adding importing modules and packages from a string
  ``container.wire(modules=["yourapp.module1"])``.
- Add container wiring configuration ``wiring_config = containers.WiringConfiguration()``.
- Add support of ``with`` statement for ``container.override_providers()`` method.
- Add ``Configuration(yaml_files=[...])`` argument.
- Add ``Configuration(ini_files=[...])`` argument.
- Add ``Configuration(pydantic_settings=[...])`` argument.
- Drop support of Python 3.4. There are no immediate breaking changes, but Dependency Injector
  will no longer be tested on Python 3.4 and any bugs will not be fixed.
- Announce the date of dropping Python 3.5 support (Jan 1st 2022).
- Fix ``Dependency.is_defined`` attribute to always return boolean value.
- Fix ``envs_required=False`` behavior in ``Configuration.from_*()`` methods
  to give a priority to the explicitly provided value.
- Update documentation and fix typos.
- Regenerate C sources using Cython 0.29.24.
- Migrate tests to ``pytest``.

4.36.2
------
- Update docs.

4.36.1
------
- Fix a wiring bug with improper resolving of ``Provide[some_provider.provider]``.
- Fix a typo in ``Factory`` provider docs ``service.add_attributes(clent=client)``
  `#499 <https://github.com/ets-labs/python-dependency-injector/issues/499>`_.
  Thanks to `@rajanjha786 <https://github.com/rajanjha786>`_ for the contribution.
- Fix a typo in ``boto3`` example
  `#511 <https://github.com/ets-labs/python-dependency-injector/issues/511>`_.
  Thanks to `@whysage <https://github.com/whysage>`_ for the contribution.

4.36.0
------
- Add support of non-string keys for ``FactoryAggregate`` provider.
- Improve ``FactoryAggregate`` typing stub.
- Improve resource subclasses typing and make shutdown definition optional
  `PR #492 <https://github.com/ets-labs/python-dependency-injector/pull/492>`_.
  Thanks to `@EdwardBlair <https://github.com/EdwardBlair>`_  for suggesting the improvement.
- Fix type annotations for ``.provides``.
  Thanks to `Thiago Hiromi @thiromi <https://github.com/thiromi>`_ for the fix
  `PR #491 <https://github.com/ets-labs/python-dependency-injector/pull/491>`_.
- Fix environment variables interpolation examples in configuration provider docs ``{$ENV} -> ${ENV}``.
  Thanks to `Felipe Rubio @krouw <https://github.com/krouw>`_ for reporting the issue and
  fixing yaml example `PR #494 <https://github.com/ets-labs/python-dependency-injector/pull/494>`_.
- Fix ``@containers.copy()`` decorator to respect dependencies on parent providers.
  See issue `#477 <https://github.com/ets-labs/python-dependency-injector/issues/477>`_.
  Thanks to `Andrey Torsunov @gtors <https://github.com/gtors>`_  for reporting the issue.
- Fix typing stub for ``container.override_providers()`` to accept other types besides ``Provider``.
- Fix runtime issue with generic typing in resource initializer classes ``resources.Resource``
  and ``resources.AsyncResource``.
  See issue `#488 <https://github.com/ets-labs/python-dependency-injector/issues/488>`_.
  Thanks to `@EdwardBlair <https://github.com/EdwardBlair>`_  for reporting the issue.

4.35.3
------
- *This release was removed from PyPI. It was inconsistently published because project has
  reached a PyPI size limit. Changes from this release are published on PyPI in next version.*

4.35.2
------
- Update wiring to support modules provided as packages.
  See issue `#481 <https://github.com/ets-labs/python-dependency-injector/issues/481>`_.
  Thanks to `@Sadbot <https://github.com/Sadbot>`_  for demonstrating the issue.

4.35.1
------
- Fix a container issue with supporting custom string types.
  See issue `#479 <https://github.com/ets-labs/python-dependency-injector/issues/479>`_.
  Thanks to `@ilsurih <https://github.com/ilsurih>`_  for reporting the issue.

4.35.0
------
- Add support of six 1.16.0.

4.34.2
------
- Fix a bug with reverse shutdown order in ``container.shutdown_resources()``.
  See issue `#432 <https://github.com/ets-labs/python-dependency-injector/issues/432>`_.
  Thanks to `Saulius Beinorius <https://github.com/saulbein>`_  for bringing up the issue.

4.34.1
------
- Update ``container.shutdown_resources()`` to respect dependencies order while shutdown.
  See issue `#432 <https://github.com/ets-labs/python-dependency-injector/issues/432>`_.
  Thanks to `Saulius Beinorius <https://github.com/saulbein>`_  for bringing up the issue.

4.34.0
------
- Add option ``envs_required`` for configuration provider ``.from_yaml()`` and ``.from_ini()``
  methods. With ``envs_required=True`` methods ``.from_yaml()`` and ``.from_ini()`` raise
  an exception when encounter an undefined environment variable in the configuration file.
  By default this option is set to false for preserving previous behavior ``envs_required=False``.
- Add raising of an exception in configuration provider strict mode when provider encounters
  an undefined environment variable in the configuration file.
- Update configuration provider environment variables interpolation to replace
  undefined environment variables with an empty value.
- Update configuration provider to perform environment variables interpolation before passing
  configuration file content to the parser.

4.33.0
------
- Add support of default value for environment variable in INI and YAML
  configuration files with ``${ENV_NAME:default}`` format.
  See issue `#459 <https://github.com/ets-labs/python-dependency-injector/issues/459>`_.
  Thanks to `Maksym Shemet @hbmshemet <https://github.com/hbmshemet>`_ for suggesting the feature.
- Add method ``Configuration.from_value()``.
  See issue `#462 <https://github.com/ets-labs/python-dependency-injector/issues/462>`_.
  Thanks to Mr. `Slack Clone <https://disqus.com/by/slackclone/>`_  for bringing it up
  in the comments for configuration provider docs.

4.32.3
------
- This fix a typo in ``di_in_python.rst`` doc.
  Thanks to `@loingo95 <https://github.com/loingo95>`_ for the fix.

4.32.2
------
- Improve wiring fault tolerance.
  See issue `#441 <https://github.com/ets-labs/python-dependency-injector/issues/441>`_.
  Thanks to `@ssheng <https://github.com/ssheng>`_ for reporting the issue.

4.32.1
------
- Fix a bug with ``List`` provider not working in async mode.
  See issue: `#450 <https://github.com/ets-labs/python-dependency-injector/issues/450>`_.
  Thanks to `@mxab <https://github.com/mxab>`_ for reporting the issue.
- Add async mode tests for ``List`` and ``Dict`` provider.

4.32.0
------
- Add ``ContextLocalSingleton`` provider.
  See PR: `#443 <https://github.com/ets-labs/python-dependency-injector/pull/442>`_.
  Thanks to `@sonthonaxrk <https://github.com/sonthonaxrk>`_ for the contribution.
- Regenerate C sources using Cython 0.29.22.

4.31.2
------
- Fix an issue with ``Dict`` provider non-string keys.
  See issue: `#435 <https://github.com/ets-labs/python-dependency-injector/issues/435>`_.
  Thanks to `@daniel55411 <https://github.com/daniel55411>`_ for reporting the issue.
- Fix Flask scoped contexts example.
  See issue: `#440 <https://github.com/ets-labs/python-dependency-injector/pull/440>`_.
  Thanks to `@sonthonaxrk <https://github.com/sonthonaxrk>`_ for the contribution.

4.31.1
------
- Fix ``ThreadSafeSingleton`` synchronization issue.
  See issue: `#433 <https://github.com/ets-labs/python-dependency-injector/issues/433>`_.
  Thanks to `@garlandhu <https://github.com/garlandhu>`_ for reporting the issue.

4.31.0
------
- Implement providers' lazy initialization.
- Improve providers' copying.
- Improve typing in wiring module.
- Fix wiring module loader uninstallation issue.
- Fix provided instance providers error handing in asynchronous mode.
- Fix overridden configuration option cache resetting.
  See issue: `#428 <https://github.com/ets-labs/python-dependency-injector/issues/428>`_.
  Thanks to `@dcendents <https://github.com/dcendents>`_ for reporting the issue.

4.30.0
------
- Remove restriction to wire a dynamic container.

4.29.2
------
- Fix wiring to not crash on missing signatures.
  See issue: `#420 <https://github.com/ets-labs/python-dependency-injector/issues/420>`_.
  Thanks to `@Balthus1989 <https://github.com/Balthus1989>`_ for reporting the issue.

4.29.1
------
- Fix recursive copying issue in ``Delegate`` provider.
  See issue: `#245 <https://github.com/ets-labs/python-dependency-injector/issues/245>`_.
  Thanks to `@GitterRemote <https://github.com/GitterRemote>`_ for reporting the issue.
- Add docs and example for ``Factory.add_attributes()`` method.
- Remove legacy css file.
- Remove ``unittest2`` test dependency.

4.29.0
------
- Implement context manager interface for resetting a singleton provider.
  See issue: `#413 <https://github.com/ets-labs/python-dependency-injector/issues/413>`_.
  Thanks to `@Arrowana <https://github.com/Arrowana>`_ for suggesting the improvement.
- Implement overriding interface to container provider.
  See issue: `#415 <https://github.com/ets-labs/python-dependency-injector/issues/415>`_.
  Thanks to `@wackazong <https://github.com/wackazong>`_ for bringing up the use case.

4.28.1
------
- Fix async mode mode exception handling issue in ``Dependency`` provider.
  See issue: `#409 <https://github.com/ets-labs/python-dependency-injector/issues/409>`_.
  Thanks to `@wackazong <https://github.com/wackazong>`_ for reporting the issue.
- Fix links to ``boto3`` example.

4.28.0
------
- Add wiring injections into modules and class attributes.
  See issue: `#411 <https://github.com/ets-labs/python-dependency-injector/issues/411>`_.
  Many thanks to `@brunopereira27 <https://github.com/brunopereira27>`_ for submitting
  the use case.

4.27.0
------
- Introduce wiring inspect filter to filter out ``flask.request`` and other local proxy objects
  from the inspection.
  See issue: `#408 <https://github.com/ets-labs/python-dependency-injector/issues/408>`_.
  Many thanks to `@bvanfleet <https://github.com/bvanfleet>`_ for reporting the issue and
  help in finding the root cause.
- Add ``boto3`` example.
- Add tests for ``.as_float()`` modifier usage with wiring.
- Make refactoring of wiring module and tests.
  See PR # `#406 <https://github.com/ets-labs/python-dependency-injector/issues/406>`_.
  Thanks to `@withshubh <https://github.com/withshubh>`_ for the contribution:
    - Remove unused imports in tests.
    - Use literal syntax to create data structure in tests.
- Add integration with a static analysis tool `DeepSource <https://deepsource.io/>`_.

4.26.0
------
- Add wiring by string id.
- Improve error message for ``Dependency`` provider missing attribute.

4.25.1
------
- Amend docs and add another example for ``@containers.copy()`` decorator.

4.25.0
------
- Add ``application-multiple-containers-runtime-overriding`` example. This example demonstrates
  how to build application from multiple containers and override one container config from
  another one in the runtime.
  See issue: `#207 <https://github.com/ets-labs/python-dependency-injector/issues/207>`_.
- Add attributes forwarding for the ``Dependency`` provider.

4.24.0
------
- Add docs on ``@containers.copy()`` decorator.
- Refactor ``@containers.copy()`` decorator.
- Refactor async mode support in containers module.

4.23.5
------
- Fix docs publishing.

4.23.4
------
- Fix a typo.

4.23.3
------
- Fix mistakenly processed awaitable objects in async mode. This bug has corrupted
  ``fastapi-redis`` example causing pool exhaustion.
  Thanks to `@iliamir <https://github.com/iliamir>`_ and Valery Komarov for finding and
  reporting the issue.
- Refactor async mode.

4.23.2
------
- Improve async mode exceptions handling.
- Fix double printing of exception when async resource initialization causes an error.

4.23.1
------
- Hotfix a bug with importing FastAPI ``Request``.
  See issue: `#398 <https://github.com/ets-labs/python-dependency-injector/issues/398>`_.
  Thanks to `@tapm <https://github.com/tapm>`_ for reporting the bug.

4.23.0
------
- Add support of aliases for ``Configuration`` provider.
  See issue: `#394 <https://github.com/ets-labs/python-dependency-injector/issues/394>`_.
  Thanks to `@gtors <https://github.com/gtors>`_ for suggesting the feature.

4.22.1
------
- Pin ``sphinx`` version to hotfix docs build.
- Fix a typo in docs.

4.22.0
------
- Add method ``container.check_dependencies()`` to check if all container dependencies
  are defined.
  See issue: `#383 <https://github.com/ets-labs/python-dependency-injector/issues/383>`_.
  Thanks to `@shaunc <https://github.com/shaunc>`_ for suggesting the feature.
- Add container name to the representation of the ``Dependency`` provider.
- Add docs cross-links between ``Singleton`` provider and "Reset container singletons"
  pages.

4.21.0
------
- Improve ``Dependency`` provider error message: when dependency is undefined,
  error message contains its name.

4.20.2
------
- Move docs on container "self" injections to "Providers" section.

4.20.1
------
- Refactor containers module.

4.20.0
------
- Add container "self" injections.
  See issue: `#364 <https://github.com/ets-labs/python-dependency-injector/issues/364>`_.
  Thanks to `@shaunc <https://github.com/shaunc>`_ for suggesting the feature.

4.19.0
------
- Add ``singleton.full_reset()`` method to reset all underlying singleton providers.
- Fix ``container.reset_singleton()`` to reset all provider types, not only ``Singleton``.
- Improve ``container.traverse(types=[...])`` and ``provider.traverse(types=[...])`` typing stubs
  to return ``types`` -typed iterator.
- Update docs on creating custom providers with a requirement to specify ``.related`` property.

4.18.0
------
- Add ``container.reset_singleton()`` method to reset container singletons.
- Refactor ``container.apply_container_providers_overridings()`` to use ``container.traverse()``.
  This enables deep lazy initialization of ``Container`` providers.
- Add tests for ``Selector`` provider.
- Add tests for ``ProvidedInstance`` and ``MethodCaller`` providers.
- Update Makefile to make Python 3 tests to be a default test command: ``make test``.

4.17.0
------
- Add ``FastAPI`` + ``SQLAlchemy`` example.
  Thanks to `@ShvetsovYura <https://github.com/ShvetsovYura>`_ for providing initial example:
  `FastAPI_DI_SqlAlchemy <https://github.com/ShvetsovYura/FastAPI_DI_SqlAlchemy>`_.

4.16.0
------
- Add container base class ``containers.Container``. ``DynamicContainer``
  and ``DeclarativeContainer`` become subclasses of the ``Container``.
  See issue: `#386 <https://github.com/ets-labs/python-dependency-injector/issues/386>`_.
  Thanks to `@ventaquil <https://github.com/ventaquil>`_ for reporting the issue.

4.15.0
------
- Add ``Configuration.from_pydantic()`` method to load configuration from a ``pydantic`` settings.

4.14.0
------
- Add container providers traversal.
- Fix an issue with ``container.init_resource()`` and ``container.shutdown_resource()`` ignoring
  nested resources that are not present on the root level.
  See issue: `#380 <https://github.com/ets-labs/python-dependency-injector/issues/380>`_.
  Thanks to `@approxit <https://github.com/approxit>`_ for finding and reporting the issue.
- Add ``.provides`` attribute to ``Singleton`` and its subclasses.
  It's a consistency change to make ``Singleton`` match ``Callable``
  and ``Factory`` interfaces.
- Add ``.initializer`` attribute to ``Resource`` provider.
- Update string representation of ``Resource`` provider.

4.13.2
------
- Fix PyCharm typing warning "Expected type 'Optional[Iterable[ModuleType]]',
  got 'List[module.py]' instead" in ``container.wire()`` method.

4.13.1
------
- Fix declarative container metaclass bug: parent container providers replaced child container providers.
  See issue: `#367 <https://github.com/ets-labs/python-dependency-injector/issues/367>`_.
  Many thanks to `Shaun Cutts <https://github.com/shaunc>`_ for finding and report the issue.

4.13.0
------
- Add ``default`` argument to the dependency provider: ``Dependency(..., default=...)``.
  See issue: `#336 <https://github.com/ets-labs/python-dependency-injector/issues/336>`_.
  Many thanks to `Shaun Cutts <https://github.com/shaunc>`_ for providing the use case.

4.12.0
------
- Add wiring import hook that auto-wires dynamically imported modules.
  See issue: `#365 <https://github.com/ets-labs/python-dependency-injector/issues/365>`_.
  Thanks to `@Balthus1989 <https://github.com/Balthus1989>`_ for providing a use case.

4.11.3
------
- Replace weakrefs with normal refs in ``ConfigurationOption`` to support
  ``Container().provider()`` use case. Test that it does not introduce a memory leak.
  See issue: `#358#issuecomment-764482059 <https://github.com/ets-labs/python-dependency-injector/issues/358#issuecomment-764482059>`_.
  Many thanks to `@Minitour <https://github.com/Minitour>`_ for reporting the issue.

4.11.2
------
- Fix a bug in ``providers.Container`` when it's declared not at class root level.
  See issue `#379 <https://github.com/ets-labs/python-dependency-injector/issues/379>`_.
  Many thanks to `@approxit <https://github.com/approxit>`_ for reporting the issue.

4.11.1
------
- Fix a bug in ``@containers.copy`` to improve replacing of subcontainer providers.
  See issue `#378 <https://github.com/ets-labs/python-dependency-injector/issues/378>`_.
  Many thanks to `Shaun Cutts <https://github.com/shaunc>`_ for reporting the issue.

4.11.0
------
- Add ``loader`` argument to the configuration provider ``Configuration.from_yaml(..., loader=...)``
  to override the default YAML loader.
  Many thanks to `Stefano Frazzetto <https://github.com/StefanoFrazzetto>`_ for suggesting an improvement.
- Make security improvement: change default YAML loader to the custom ``yaml.SafeLoader`` with a support
  of environment variables interpolation.
  Many thanks to `Stefano Frazzetto <https://github.com/StefanoFrazzetto>`_ for suggesting an improvement.
- Update configuration provider ``.from_*()`` methods to raise an exception in strict mode if
  configuration file does not exist or configuration data is undefined.
  Many thanks to `Stefano Frazzetto <https://github.com/StefanoFrazzetto>`_ for suggesting an improvement.
- Add ``required`` argument to the configuration provider ``.from_*()`` methods to specify
  mandatory configuration sources.
  Many thanks to `Stefano Frazzetto <https://github.com/StefanoFrazzetto>`_ for suggesting an improvement.
- Fix a bug with asynchronous injections: async providers do not work with async dependencies.
  See issue: `#368 <https://github.com/ets-labs/python-dependency-injector/issues/368>`_.
  Thanks `@kolypto <https://github.com/kolypto>`_ for the bug report.
- Refactor asynchronous injections.
- Add extra tests for asynchronous injections.
- Migrate CI to Github Actions.

4.10.3
------
- Fix a bug in the ``Configuration`` provider: strict mode didn't work when provider
  is overridden by ``None``.
  See issue: `#358#issuecomment-761607432 <https://github.com/ets-labs/python-dependency-injector/issues/358#issuecomment-761607432>`_.
  Many thanks to `Stefano Frazzetto <https://github.com/StefanoFrazzetto>`_ for reporting the issue.

4.10.2
------
- Fix a bug in ``Resource`` that cause failure when async resource depends on
  another async resource.
  See issue `#361 <https://github.com/ets-labs/python-dependency-injector/issues/361>`_.
  Thanks `@kolypto <https://github.com/kolypto>`_ for the bug report.

4.10.1
------
- Fix a Python 3.9 specific bug in ``wiring`` module: introspection doesn't work for
  builtin ``types.GenericAlias``. This resulted in wiring failure for modules
  importing ``queue.Queue``.
  See issue `#362 <https://github.com/ets-labs/python-dependency-injector/issues/362>`_.
  Thanks `@ventaquil <https://github.com/ventaquil>`_ for the bug report.
- Switch Coveralls reporting Travis Job to run on Python 3.9.

4.10.0
------
- Add ``strict`` mode and ``required`` modifier for ``Configuration`` provider.
  See issue `#341 <https://github.com/ets-labs/python-dependency-injector/issues/341>`_.
  Thanks `ms-lolo <https://github.com/ms-lolo>`_ for the feature request.

4.9.1
-----
- Fix a bug in the ``Configuration`` provider to correctly handle undefined values.
  See issue `#358 <https://github.com/ets-labs/python-dependency-injector/issues/358>`_.
  Many thanks to `Stefano Frazzetto <https://github.com/StefanoFrazzetto>`_ for reporting the issue.

4.9.0
-----
- Add ``.dependencies`` attribute to the ``DeclarativeContainer`` and ``DynamicContainer``.
  It returns dictionary of container ``Dependency`` and ``DependenciesContainer`` providers.
  See issue `#357 <https://github.com/ets-labs/python-dependency-injector/issues/357>`_.
  Many thanks to `Shaun Cutts <https://github.com/shaunc>`_ for suggesting the feature.

4.8.3
-----
- Fix a bug in the ``Configuration`` provider to correctly handle overriding by ``None``.
  See issue `#358 <https://github.com/ets-labs/python-dependency-injector/issues/358>`_.
  Many thanks to `Stefano Frazzetto <https://github.com/StefanoFrazzetto>`_ for reporting the issue.

4.8.2
-----
- Fix ``Container`` provider to apply context overridings on root container initialization.
  See issue `#354 <https://github.com/ets-labs/python-dependency-injector/issues/354>`_.
  Many thanks to `Shaun Cutts <https://github.com/shaunc>`_ for submitting the issue.
- Hotfix for version ``4.8.0``: fix side effect in ``Container`` provider overriding.

4.8.1
-----
- Fix declarative container multi-level inheritance issue.
  See issue `#350 <https://github.com/ets-labs/python-dependency-injector/issues/350>`_.
  Many thanks to `Shaun Cutts <https://github.com/shaunc>`_ for submitting the issue.

4.8.0
-----
- Add support of overriding ``Container`` provider.
  See issue `#354 <https://github.com/ets-labs/python-dependency-injector/issues/354>`_.
  Many thanks to `Shaun Cutts <https://github.com/shaunc>`_ for submitting the issue.

4.7.0
-----
- Add container injection support for wiring.

4.6.1
-----
- Add Disqus comments widget to the provider's async injections docs page.

4.6.0
-----
- Add support of async injections for providers.
- Add support of async injections for wiring.
- Add support of async initializers for ``Resource`` provider.
- Add ``FastAPI`` + ``Redis`` example.
- Add ARM wheel builds.
  See issue `#342 <https://github.com/ets-labs/python-dependency-injector/issues/342>`_ for details.
- Fix a typo in `ext.flask` deprecation warning.
  See PR `#345 <https://github.com/ets-labs/python-dependency-injector/pull/345>`_ for details.
  Thanks to `Fotis Koutoupas <https://github.com/kootoopas>`_ for the fix.
- Update copyright year.

4.5.4
-----
- Fix manylinux wheels uploading issue.
  See issue `#333 <https://github.com/ets-labs/python-dependency-injector/issues/333>`_ for details.
  Thanks to `Richard Jones <https://github.com/RichardDRJ>`_ for reporting the issue.

4.5.3
-----
- Fix ``4.5.2`` degradation bug in wiring ``@inject`` with not working ``FastAPI.Depends`` directive.
  See issue `#331 <https://github.com/ets-labs/python-dependency-injector/issues/331>`_ for details.
  Thanks to `Juan Esteban Marín <https://github.com/juanmarin96>`_ for reporting the issue.
- Add ``FastAPI`` tests.

4.5.2
-----
- Fix a bug in wiring ``@inject`` with not properly working ``FastAPI.Depends`` directive.
  See issue `#330 <https://github.com/ets-labs/python-dependency-injector/issues/330>`_ for details.
  Thanks to `Lojka-oops <https://github.com/Lojka-oops>`_ for reporting the issue.

4.5.1
-----
- Fix flake8 issue in ``Commands  and Handlers`` example.

4.5.0
-----
- Add support of non-string keys for ``Dict`` provider.
- Add simple ``FastAPI`` example.
- Add ``Commands  and Handlers`` example from
  issue `#327 <https://github.com/ets-labs/python-dependency-injector/issues/327>`_.
- Add extra typing test for provided instance of ``DependenciesContainer`` provider.

4.4.1
-----
- Improve ``FastAPI`` integration: handle ``Depends(Provide[...])``.
- Update ``FastAPI`` example.
- Remove a typo from the ``Flask`` tutorial.

4.4.0
-----
- Add ``@inject`` decorator. It helps to fix a number of wiring bugs and make wiring be more resilient.
- Refactor ``wiring`` module.
- Update documentation and examples to use ``@inject`` decorator.
- Add ``Flask`` blueprints example.
- Fix wiring bug when wiring doesn't work with the class-based decorators.
- Fix wiring bug when wiring doesn't work with the decorators that doesn't use ``functools.wraps(...)``.
- Fix wiring bug with ``@app.route(...)`` -style decorators (Flask, Sanic, FastAPI, etc.).
- Fix wiring bug when wiring doesn't work with Flask blueprints.

4.3.9
-----
- Add ``FastAPI`` example.

4.3.8
-----
- Add a hotfix to support wiring for ``FastAPI`` endpoints.

4.3.7
-----
- Fix race in ``ThreadSafeSingleton``. Many thanks to
  `Dmitry Rassoshenko aka rda-dev <https://github.com/rda-dev>`_ for the pull request
  (See PR `#322 <https://github.com/ets-labs/python-dependency-injector/pull/322>`_).

4.3.6
-----
- Fix changelog typo.

4.3.5
-----
- Fix a bug in ``wiring`` module that caused multiple imports of the modules
  when ``.wire(packages=[...])`` is used
  (See issue `#320 <https://github.com/ets-labs/python-dependency-injector/issues/320>`_). Thanks
  to `Federico iskorini <https://github.com/iskorini>`_ for reporting the issue.

4.3.4
-----
- Fix a bug in ``Configuration`` provider that resulted in not working ``.reset_override()``
  (See issue `#319 <https://github.com/ets-labs/python-dependency-injector/issues/319>`_). Thanks
  to `Jun lust4life <https://github.com/lust4life>`_ for reporting the issue and suggesting a fix.

4.3.3
-----
- Fix a bug in ``wiring`` with improper patching of ``@classmethod`` and ``@staticmethod`` decorated methods
  (See issue `#318 <https://github.com/ets-labs/python-dependency-injector/issues/318>`_).

4.3.2
-----
- Fix a bug in ``wiring`` with mistakenly initialized and shutdown resource with ``Closing``
  marker on context argument providing.

4.3.1
-----
- Fix README.

4.3.0
-----
- Implement per-function execution scope for ``Resource`` provider in tandem
  with ``wiring.Closing``.

4.2.0
-----
- Add support of Python 3.9.
- Update readme.

4.1.8
-----
- Update asyncio daemon, single- and multi-container examples to use ``Resource`` provider.

4.1.7
-----
- Add CI job to build and push documentation to S3 bucket.

4.1.6
-----
- Fix wiring of multiple containers
  (see issue `#313 <https://github.com/ets-labs/python-dependency-injector/issues/313>`_).
  Thanks to `iskorini <https://github.com/iskorini>`_ for reporting the  issue.
- Fix wiring for ``@classmethod``.

4.1.5
-----
- Fix Travis CI windows and MacOS builds.

4.1.4
-----
- Fix version of ``cibuildwheel==1.63``.
- Update Travis CI webhooks to fix builds triggering.

4.1.3
-----
- Migrate from ``travis-ci.org`` to ``travis-ci.com`` to fix build issues.
- Add explicit installation of ``certifi`` for Windows build to resolve build problems.

4.1.2
-----
- Bump version of ``cibuildwheel>=1.5.1`` to resolve Windows build problem.

4.1.1
-----
- Fix a few typos in ``Resource`` provider docs.

4.1.0
-----
- Add ``Resource`` provider.
- Add ``Dict`` provider.
- "Un-deprecate" ``@containers.override()`` and ``@containers.copy()`` decorators (
  see `Issue 301 <https://github.com/ets-labs/python-dependency-injector/issues/301>`_
  for more information).
- Add favicon.
- Remove redirects that occur while getting badge images to optimize docs load speed.
- Update license year.
- Update short description on PyPI.

4.0.6
-----
- Fix wiring for top-level package ``__init__.py``.

4.0.5
-----
- Move ``.provided`` attribute to ``providers.Provider``.
- Update all links in documentation and examples to use ``https://`` instead of ``http``.

4.0.4
-----
- Fix typing stubs for ``container.override()`` method.

4.0.3
-----
- Deprecate ``@containers.override()`` and ``@containers.copy()`` decorators.
- Update changelog of version ``4.0.0`` so it lists all deprecated features.

4.0.2
-----
- Fix typing stubs for ``@container.override()`` and ``@containers.copy()`` decorators (
  see `PR 302 <https://github.com/ets-labs/python-dependency-injector/pull/302>`_). Thanks
  to `JarnoRFB <https://github.com/JarnoRFB>`_ for reporting the issue.

4.0.1
-----
- Extend ``Configuration.from_ini()`` and ``Configuration.from_yaml()`` typing stubs to
  accept ``pathlib.Path``. The methods were already compatible with ``pathlib.Path``
  and just did not accept it in their signatures (see
  `PR 300 <https://github.com/ets-labs/python-dependency-injector/pull/300>`_). Fix
  was provided by `JarnoRFB <https://github.com/JarnoRFB>`_. Many thanks to you again,
  JarnoRFB.

4.0.0
-----
New features:

- Add ``wiring`` feature.

Deprecations:

- Deprecate ``ext.aiohttp`` module in favor of ``wiring`` feature.
- Deprecate ``ext.flask`` module in favor of ``wiring`` feature.
- Deprecate ``.delegate()`` provider method in favor of ``.provider`` attribute.

Removals:

- Remove deprecated ``types`` module.

Tutorials:

-  Update ``flask`` tutorial.
-  Update ``aiohttp`` tutorial.
-  Update ``asyncio`` daemon tutorial.
-  Update CLI application tutorial.

Examples:

- Add ``django`` example.
- Add ``sanic`` example.
- Update ``aiohttp`` example.
- Update ``flask`` example.
- Update ``asyncio`` daemon example.
- Update ``movie-lister`` example.
- Update CLI application example.

Misc:

- Regenerate C sources using Cython 0.29.21.
- Improve documentation and README (typos removal, rewording, etc).

3.44.0
------
- Add native support of the generics to the providers: ``some_provider = providers.Provider[SomeClass]``.
- Deprecate module ``types``.
- Add documentation page on providers typing and ``mypy`` support.
- Update README.

3.43.1
------
- Fix a typo in README.

3.43.0
------
- Update API documentation.
- Remove not relevant "speech" example.
- Fix a few typos.

3.42.0
------
- Update "DI in Python" documentation page.
- Delete "What is DI?" documentation page.
- Delete "engines cars" example mini app.
- Update README.

3.41.0
------
- Refactor "use cases" example.
- Refactor "password hashing" example.
- Refactor "chained factories" pattern example.
- Refactor "factory of factories" pattern example.
- Fix declarative container mypy stub to ``__init__`` to accept not only providers.
- Refactor main module of the "decoupled packages" example.
- Delete "api client" example mini app.
- Delete "mail service" example mini app.

3.40.0
------
- Add "Decoupled packages" example.
- Delete "Bundles" examples mini application.

3.39.0
------
- Add application examples with single and multiple containers.
- Remove "Services" application examples.
- Split examples page into "Examples" with main examples and "Other Examples" with secondary
  examples.
- Move "Installation" page to "Introduction" section.

3.38.1
------
- Fix README.

3.38.0
------
- Update "What is What is dependency injection?" documentation page.
- Update README.
- Fix a bunch of typos.

3.37.0
------
- Update index documentation page.
- Make multiple improvements and fixes for the providers documentation.
- Update "Key Features" documentation page.
- Remove "Structure of Dependency Injector" documentation page.
- Edit "Feedback" documentation page.

3.36.0
------
- Update providers overriding documentation and rework examples.
- Update documentation on injecting provided object attributes, items or method calls.
- Update documentation and example on creating a custom provider.
- Update providers index documentation page to give better overview of providers functionality.
- Fix mypy stub of the ``Provider`` to specify the protected ``._copy_overridings()`` method.
- Update copyright year in the documentation.

3.35.1
------
- Fix minor issues in the providers documentation and examples.

3.35.0
------
- Update documentation and rework examples for: ``Singleton``, ``Callable``, ``Coroutine``,
  ``Object``, ``List``, ``Configuration``, ``Selector``, and ``Dependency`` providers.
- Fix mypy stub of the ``DeclarativeContainer`` to specify the ``__init__`` interface.

3.34.0
------
- Update ``Factory`` provider documentation.
- Rework ``Factory`` provider examples.

3.33.0
------
- Add typing stubs.

3.32.3
------
- Fix few typos on README and docs main pages.

3.32.2
------
- Make a fix in the factory delegation example (thanks to
  `Joël Bourgault <https://github.com/ojob>`_ for finding and reporting the issue).

3.32.1
------
- Update DI Demo 2 example and READ to make typed configuration option injection.

3.32.0
------
- Add a feature that helps to explicitly specify the type of the configuration option value
  before the injection.
- Add disqus comments to the docs page on injecting provided instance attributes, items, etc.

3.31.0
------
- Add a feature that helps to inject provided instance attribute, item, or method call result
  (see `Issue 281 <https://github.com/ets-labs/python-dependency-injector/issues/281>`_). Design
  for this feature was provided by `JarnoRFB <https://github.com/JarnoRFB>`_. Many thanks to you,
  JarnoRFB.

3.30.4
------
- Update README.

3.30.3
------
- Update README.
- Update containers documentation and examples.

3.30.2
------
- Update README.

3.30.1
------
- Update README.
- Add one more example.

3.30.0
------
- Rework ``Movie Lister`` example.
- Add tutorial for building ``Movie Lister``.
- Make some rewording for the other tutorials.
- Fix a couple of typos.

3.29.0
------
- Update README with the more direct message on what is ``Dependency Injector`` and how is it
  different from the other frameworks.
- Change the example code in the README.
- Add FAQ to the README.
- Update documentation key features and index pages.

3.28.1
------
- Fix typos in the ``asyncio`` + ``Dependency Injector`` monitoring daemon tutorial.

3.28.0
------
- Add ``asyncio`` + ``Dependency Injector`` example ``monitoring-daemon-asyncio``.
- Add ``asyncio`` + ``Dependency Injector`` monitoring daemon tutorial.
- Fix a typo in the docblock of the ``Configuration`` provider.
- Fix multiple typos in the ``flask`` and ``aiohttp`` tutorials.
- Fix ``Makefile`` to run ``aiohttp`` integration tests on Python 3.5+.

3.27.0
------
- Add deep init injections overriding for ``Factory`` provider.
- Add ``asyncio`` monitoring daemon example.

3.26.0
------
- Add configuration itemselector feature (see
  `Issue 274 <https://github.com/ets-labs/python-dependency-injector/issues/274>`_).
- Re-design ``Configuration`` provider implementation.
- Update ``giphynav-aiohttp`` to remove doubled "if not query" (many thanks to
  `Oleg Baranov <https://github.com/mrbish>`_ for the feedback).

3.25.1
------
- Fix ``aiohttp`` tutorial typos.

3.25.0
------
- Add ``aiohttp`` tutorial.
- Fix ``Flask`` tutorial typos and change some wording.

3.24.1
------
- Update Google Search Console verification meta tag.
- Update meta description.

3.24.0
------
- Add ``Aiohttp`` integration module ``dependency_injector.ext.aiohttp``.
- Add ``Aiohttp`` + ``Dependency Injector`` example ``giphynav-aiohttp``.

3.23.2
------
- Fix ``Flask`` tutorial code issues, typos and change some wording.

3.23.1
------
- Fix an issue with creating ``Dependency`` provider with ``abc.ABCMeta``.
  Thanks to `awaizman1 <https://github.com/awaizman1>`_. More info:
  `Issue #266 <https://github.com/ets-labs/python-dependency-injector/issues/266>`_,
  `PR #267 <https://github.com/ets-labs/python-dependency-injector/pull/267>`_.

3.23.0
------
- Add ``Flask`` tutorial.
- Add PyPI classifiers.

3.22.0
------
- Migrate docs to ``alabaster`` theme.
- Add ``Bootstrap`` extension to the ``ghnav-flask`` example.
- Add stubs for the tutorials to the docs.

3.21.2
------
- Hotfix changelog typo.

3.21.1
------
- Hotfix ``ghnav-flask`` example to read Github token from environment variable.

3.21.0
------
- Re-design ``Flask`` integration.
- Make cosmetic fixes for ``Selector`` provider docs.

3.20.1
------
- Hotfix Windows builds.

3.20.0
------
- Add ``Flask`` integration module ``dependency_injector.ext.flask``.
- Add ``Flask`` + ``Dependency Injector`` example ``ghnav-flask``.
- Add ``Factory.provides`` attribute. It is an alias to the ``Factory.cls``.
- New README.

3.19.2
------
- Add logo.

3.19.1
------
- Start distributing wheels for Linux, MacOS, and Windows (thanks to
  `Travis CI <https://travis-ci.org/>`_ and
  `cibuildwheel <https://github.com/joerick/cibuildwheel>`_).
- Start using ``twine`` for publishing package on PyPI.
- Fix Travis CI configuration file warnings.

3.19.0
------
- Add ``Selector`` provider.
- Fix ``Configuration.override()`` to return ``OverridingContext`` for non-dictionary values.

3.18.1
------
- Add interpolation of environment variables to ``Configuration.from_yaml()`` and
  ``Configuration.from_ini()``.
- Add ignoring of ``IOError`` to ``Configuration.from_yaml()``.

3.18.0
------
- Add ``Configuration.from_yaml()`` method to load configuration from the yaml file.
- Add ``Configuration.from_ini()`` method to load configuration from the ini file.
- Add ``Configuration.from_dict()`` method to load configuration from the dictionary.
- Add ``Configuration.from_env()`` method to load configuration from the environment variable.
- Add default value for ``name`` argument of ``Configuration`` provider.
- Add documentation for ``Configuration`` provider.
- Remove undocumented positional parameter of ``DependenciesContainer`` provider.

3.17.1
------
- Fix ``DynamicContainer`` deep-copying bug.

3.17.0
------
- Add ``Container`` provider.
- Add ``Configuration`` providers linking.

3.16.1
------
- Update ``singleton_thread_locals.py`` to support Python 3 (thanks to
  `RobinsonMa <https://github.com/RobinsonMa>`_,
  `PR #252 <https://github.com/ets-labs/python-dependency-injector/pull/252>`_).
- Fix Disqus comments.
- Fix warnings in API docs.

3.16.0
------
- Add ``List`` provider
  `issue #243 <https://github.com/ets-labs/python-dependency-injector/issues/243>`_,
  `PR #251 <https://github.com/ets-labs/python-dependency-injector/pull/251>`_.
- Fix a few typos in docs (thanks to `Bruno P. Kinoshita <https://github.com/kinow>`_,
  `issue #249 <https://github.com/ets-labs/python-dependency-injector/issues/249>`_,
  `PR #250 <https://github.com/ets-labs/python-dependency-injector/pull/250>`_).
- Add support of six 1.15.0.
- Regenerate C sources using Cython 0.29.20.

3.15.6
------
- Fix changelog typo.

3.15.5
------
- Add downloads badge.

3.15.4
------
- Update a link to the PyPi page on the README page.

3.15.3
------
- Fix a typo in the link to the PyPi on the "Dependency Injection in Python" documentation page.
- Fix a couple of typos in the list of key features on the "Key Features" and index documentation
  pages.
- Update a link to the PyPi page on a couple of documentation pages.

3.15.2
------
- Fix a typo in the installation instructions on the README page and in the documentation.

3.15.1
------
- Fix a couple of typos in the README.
- Fix a couple of types in the diagram of "Engines-Cars" example.

3.15.0
------
- Add Python 3.8 support.
- Add PyPy 3.6 support.
- Add support of six 1.14.0.
- Add support of six 1.13.0.
- Regenerate C sources using Cython 0.29.14.
- Remove Python 2-ish inheritance from ``object`` in example modules.
- Replace Python 2-ish ``super(class, self).__init__()`` calls with Python 3-ish
  ``super().__init__()`` in example modules.
- Fix doc block errors in example modules, including related to PEP257-compliance.
- Clean up tox.ini file.

3.14.12
-------
- Fix ``3.14.11`` degradation issue causing inability of using ``Delegate`` provider in
  ``DeclarativeContainer`` when this container is instantiated with overriding of delegating
  provider (thanks to `GitterRemote <https://github .com/GitterRemote>`_, issue details are here
  `#235 <https://github.com/ets-labs/python-dependency-injector/issues/235>`_).

3.14.11
-------
- Fix issue causing creation of a copy of provided object by ``Object`` provider when it was a
  part of ``DeclarativeContainer`` and this container was instantiated (thanks to
  `davidcim <https://github.com/davidcim>`_, issue details are here
  `#231 <https://github.com/ets-labs/python-dependency-injector/issues/231>`_).

3.14.10
-------
- Make spelling fix for the list of contributors.

3.14.9
------
- Improve README - minor English nitpicking (thanks to `supakeen <https://github.com/supakeen>`_).

3.14.8
------
- Regenerate C sources using Cython 0.29.13.

3.14.7
------
- Fix typo on "Dependency injection and inversion of control in Python" docs page (thanks to
  `Dmitry (xotonic) <https://github.com/xotonic>`_).

3.14.6
------
- Fix ``FactoryAggregate`` provider copying issue.
- Regenerate C sources using Cython 0.29.7.

3.14.5
------
- Fix issue causing ``ThreadLocalSingleton`` provider to return ``None`` after
  reset (thanks to `Jeroen Rietveld <https://github.com/jeroenrietveld>`_).
- Add test for ``ThreadLocalSingleton`` provider reset functionality (thanks
  to `Jeroen Rietveld <https://github.com/jeroenrietveld>`_).
- Regenerate C sources using Cython 0.29.6.


3.14.4
------
- Fix typo in providers doc (thanks to `Vlad Ghita <https://github.com/vlad-ghita>`_).

3.14.3
------
- Fix issue with copying providers that have  system streams injections
  (``sys.stdin``, ``sys.stdout`` and ``sys.stderr``).
- Add support of six 1.12.0.
- Regenerate C sources using Cython 0.29.2.

3.14.2
------
- Set Cython ``language_level=2``.

3.14.1
------
- Fix bug `#208 <https://github.com/ets-labs/python-dependency-injector/issues/208>`_:
  version ``3.14.0`` hasn't worked on Python 3.5.2 (thanks to
  `Jeroen Entjes <https://github.com/JeroenEntjes>`_).
- Remove deprecated ``assertEquals`` from tests.
- Regenerate C sources using Cython 0.29.

3.14.0
------
- Add ``Coroutine`` provider.
- Add ``DelegatedCoroutine`` provider.
- Add ``AbstractCoroutine`` provider.
- Add ``CoroutineDelegate`` provider.
- Fix type-hinting of ``*args`` & ``**kwargs`` that was specified in doc
  blocks of various providers and caused inspection problems in PyCharm.
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
  3.3.6 - special attributes were identified by formula ``__{text}`` - now
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

  1. Module ``dependency_injector.containers`` was split into submodules
     without any functional changes.

- **Utils**

  1. Module ``dependency_injector.utils`` is split into
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
  will be removed in further releases.
- ``@inject`` decorator was refactored to keep all injections in
  ``_injections`` attribute of decorated callback. It will give a possibility to
  track all the injections of particular callbacks and gives some performance
  boost due minimizing number of calls for doing injections.
- A lot of documentation updates were made.
- A lot of examples were added.
- Some minor refactorings were done.

Previous versions
-----------------

- While *Objects* was in alpha state, changes were not tracked.

.. disqus::


.. _Semantic versioning: https://semver.org/
