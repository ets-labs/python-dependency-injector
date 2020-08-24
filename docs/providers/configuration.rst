Configuration providers
-----------------------

.. currentmodule:: dependency_injector.providers

:py:class:`Configuration` provider provides configuration options to the other providers.

.. literalinclude:: ../../examples/providers/configuration/configuration.py
   :language: python
   :emphasize-lines: 4,9-10
   :lines: 4-14

It implements "use first, define later" principle.

Loading from ``ini`` file
~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Configuration` provider can load configuration from ``ini`` file using
:py:meth:`Configuration.from_ini`:

.. literalinclude:: ../../examples/providers/configuration/configuration_ini.py
   :language: python
   :lines: 3-5,6-
   :emphasize-lines: 6

where ``examples/providers/configuration/config.ini`` is:

.. literalinclude:: ../../examples/providers/configuration/config.ini
   :language: ini

:py:meth:`Configuration.from_ini` supports environment variables interpolation. Use
``${ENV_NAME}`` format in the configuration file to substitute value of environment
variable ``ENV_NAME``.

Loading from ``yaml`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Configuration` provider can load configuration from ``yaml`` file using
:py:meth:`Configuration.from_yaml`:

.. literalinclude:: ../../examples/providers/configuration/configuration_yaml.py
   :language: python
   :lines: 3-5,6-
   :emphasize-lines: 6

where ``examples/providers/configuration/config.yml`` is:

.. literalinclude:: ../../examples/providers/configuration/config.yml
   :language: ini

:py:meth:`Configuration.from_yaml` supports environment variables interpolation. Use
``${ENV_NAME}`` format in the configuration file to substitute value of environment
variable ``ENV_NAME``.

.. note::

    Loading configuration from yaml requires ``PyYAML`` package. You can install
    `Dependency Injector` with extras ``pip install dependency-injector[yaml]`` or install
    ``PyYAML`` separately  ``pip install pyyaml``.

Loading from ``dict``
~~~~~~~~~~~~~~~~~~~~~

:py:class:`Configuration` provider can load configuration from Python ``dict`` using
:py:meth:`Configuration.from_dict`:

.. literalinclude:: ../../examples/providers/configuration/configuration_dict.py
   :language: python
   :lines: 3-5,6-
   :emphasize-lines: 6-13

Loading from environment variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Configuration` provider can load configuration from environment variable using
:py:meth:`Configuration.from_env`:

.. literalinclude:: ../../examples/providers/configuration/configuration_env.py
   :language: python
   :lines: 5-7,13-21
   :emphasize-lines: 6-8

Loading from multiple sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`Configuration` provider can load configuration from multiple sources. Loaded
configuration is merged recursively over existing configuration.

.. literalinclude:: ../../examples/providers/configuration/configuration_multiple.py
   :language: python
   :lines: 3-5,6-14
   :emphasize-lines: 6-7

where ``examples/providers/configuration/config.local.yml`` is:

.. literalinclude:: ../../examples/providers/configuration/config.local.yml
   :language: ini

Specifying value type
~~~~~~~~~~~~~~~~~~~~~

You can specify the type of the injected configuration value explicitly.

This helps when you read the value from the ini file or the environment variable and need to
convert it into an ``int`` or a ``float``.

.. literalinclude:: ../../examples/providers/configuration/configuration_type.py
   :language: python
   :lines: 3-
   :emphasize-lines: 17

:py:class:`Configuration` provider has next helper methods:

- ``.as_int()``
- ``.as_float()``
- ``.as_(callback, *args, **kwargs)``

The last method ``.as_(callback, *args, **kwargs)`` helps to implement a other conversions.

.. literalinclude:: ../../examples/providers/configuration/configuration_type_custom.py
   :language: python
   :lines: 3-
   :emphasize-lines: 16

With the ``.as_(callback, *args, **kwargs)`` you can specify the function that will be called
before the injection. The value from the config will be passed as a first argument. The returned
value will be injected. Parameters ``*args`` and ``**kwargs`` are handled as any other injections.

.. disqus::
