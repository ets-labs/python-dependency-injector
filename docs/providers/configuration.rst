Configuration provider
======================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Configuration,Injection,
              Option,Ini,Json,Yaml,Dict,Environment Variable,Load,Read,Get
   :description: Configuration provides configuration options to the other providers. This page
                 demonstrates how to use Configuration provider to inject the dependencies, load
                 a configuration from an ini or yaml file, dictionary or an environment variable.

.. currentmodule:: dependency_injector.providers

:py:class:`Configuration` provider provides configuration options to the other providers.

.. literalinclude:: ../../examples/providers/configuration/configuration.py
   :language: python
   :emphasize-lines: 4,9-10
   :lines: 4-14

It implements the principle "use first, define later".

Loading from an INI file
------------------------

``Configuration`` provider can load configuration from an ``ini`` file using the
:py:meth:`Configuration.from_ini` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_ini.py
   :language: python
   :lines: 3-5,6-
   :emphasize-lines: 6

where ``examples/providers/configuration/config.ini`` is:

.. literalinclude:: ../../examples/providers/configuration/config.ini
   :language: ini

:py:meth:`Configuration.from_ini` method supports environment variables interpolation. Use
``${ENV_NAME}`` format in the configuration file to substitute value of the environment
variable ``ENV_NAME``.

Loading from a YAML file
------------------------

``Configuration`` provider can load configuration from a ``yaml`` file using the
:py:meth:`Configuration.from_yaml` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_yaml.py
   :language: python
   :lines: 3-5,6-
   :emphasize-lines: 6

where ``examples/providers/configuration/config.yml`` is:

.. literalinclude:: ../../examples/providers/configuration/config.yml
   :language: ini

:py:meth:`Configuration.from_yaml` method supports environment variables interpolation. Use
``${ENV_NAME}`` format in the configuration file to substitute value of the environment
variable ``ENV_NAME``.

.. note::

   Loading of a yaml configuration requires ``PyYAML`` package.

   You can install the ``Dependency Injector`` with an extra dependency::

      pip install dependency-injector[yaml]

   or install ``PyYAML`` directly::

      pip install pyyaml

   *Don't forget to mirror the changes in the requirements file.*

Loading from a dictionary
-------------------------

``Configuration`` provider can load configuration from a Python ``dict`` using the
:py:meth:`Configuration.from_dict` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_dict.py
   :language: python
   :lines: 3-5,6-
   :emphasize-lines: 6-13

Loading from an environment variable
------------------------------------

``Configuration`` provider can load configuration from an environment variable using the
:py:meth:`Configuration.from_env` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_env.py
   :language: python
   :lines: 5-7,13-21
   :emphasize-lines: 6-8

Loading from the multiple sources
---------------------------------

``Configuration`` provider can load configuration from the multiple sources. Loaded
configuration is merged recursively over the existing configuration.

.. literalinclude:: ../../examples/providers/configuration/configuration_multiple.py
   :language: python
   :lines: 3-5,6-14
   :emphasize-lines: 6-7

where ``examples/providers/configuration/config.local.yml`` is:

.. literalinclude:: ../../examples/providers/configuration/config.local.yml
   :language: ini

Specifying the value type
-------------------------

You can specify the type of the injected configuration value explicitly.

This helps when you read the value from an ini file or an environment variable and need to
convert it into an ``int`` or a ``float``.

.. literalinclude:: ../../examples/providers/configuration/configuration_type.py
   :language: python
   :lines: 3-
   :emphasize-lines: 17

``Configuration`` provider has next helper methods:

- ``.as_int()``
- ``.as_float()``
- ``.as_(callback, *args, **kwargs)``

The last method ``.as_(callback, *args, **kwargs)`` helps to implement other conversions.

.. literalinclude:: ../../examples/providers/configuration/configuration_type_custom.py
   :language: python
   :lines: 3-
   :emphasize-lines: 16

With the ``.as_(callback, *args, **kwargs)`` you can specify a function that will be called
before the injection. The value from the config will be passed as a first argument. The returned
value will be injected. Parameters ``*args`` and ``**kwargs`` are handled as any other injections.

.. disqus::
