Changelog
=========

This document describes all the changes in *Objects* framework that were made
in every particular version.

From version 0.7.6 *Objects* framework strictly follows `Semantic versioning`_


Development version
-------------------

- No features.

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
