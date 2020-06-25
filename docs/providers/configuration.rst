Configuration providers
-----------------------

.. currentmodule:: dependency_injector.providers

:py:class:`Configuration` provider provides configuration options to the other providers.

.. literalinclude:: ../../examples/providers/configuration/configuration.py
   :language: python
   :emphasize-lines: 7,12-13,18-25
   :linenos:

It implements "use first, define later" principle.

Loading from ``ini`` file
~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Configuration` provider can load configuration from ``ini`` file using
:py:meth:`Configuration.from_ini`:

.. literalinclude:: ../../examples/providers/configuration/configuration_ini.py
   :language: python
   :lines: 6-
   :emphasize-lines: 3
   :linenos:

where ``examples/providers/configuration/config.ini`` is:

.. literalinclude:: ../../examples/providers/configuration/config.ini
   :language: ini
   :linenos:

Loading from ``yaml`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Configuration` provider can load configuration from ``yaml`` file using
:py:meth:`Configuration.from_yaml`:

.. literalinclude:: ../../examples/providers/configuration/configuration_yaml.py
   :language: python
   :lines: 6-
   :emphasize-lines: 3
   :linenos:

where ``examples/providers/configuration/config.yml`` is:

.. literalinclude:: ../../examples/providers/configuration/config.yml
   :language: ini
   :linenos:

.. note::

    Loading configuration from yaml requires ``PyYAML`` package. You can install
    `Dependency Injector` with extras ``pip install dependency-injector[yaml]`` or install
    ``PyYAML`` separately  ``pip install pyyaml``.

Loading from environment variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Configuration` provider can load configuration from environment variable using
:py:meth:`Configuration.from_env`:

.. literalinclude:: ../../examples/providers/configuration/configuration_env.py
   :language: python
   :lines: 13-21
   :emphasize-lines: 3-5
   :linenos:


Loading from multiple sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Configuration` provider can load configuration from multiple sources. Loaded
configuration is merged recursively over existing configuration.

.. literalinclude:: ../../examples/providers/configuration/configuration_multiple.py
   :language: python
   :lines: 6-14
   :emphasize-lines: 3-4
   :linenos:

where ``examples/providers/configuration/config.local.yml`` is:

.. literalinclude:: ../../examples/providers/configuration/config.local.yml
   :language: ini
   :linenos:

.. disqus::
