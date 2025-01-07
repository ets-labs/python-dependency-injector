.. _configuration-provider:

Configuration provider
======================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Configuration,Injection,
              Option,Ini,Json,Yaml,Pydantic,Dict,Environment Variable Interpolation,
              Environment Variable Substitution,Environment Variable in Config,
              Environment Variable in YAML file,Environment Variable in INI file,Default,Load,Read
   :description: Configuration provides configuration options to the other providers. This page
                 demonstrates how to use Configuration provider to inject the dependencies, load
                 a configuration from an ini or yaml file, a dictionary, an environment variable,
                 or a pydantic settings object. This page also describes how to substitute (interpolate)
                 environment variables in YAML and INI configuration files.

.. currentmodule:: dependency_injector.providers

:py:class:`Configuration` provider provides configuration options to the other providers.

.. literalinclude:: ../../examples/providers/configuration/configuration.py
   :language: python
   :emphasize-lines: 7,12-13
   :lines: 3-

It implements the principle "use first, define later".

.. contents::
   :local:
   :backlinks: none

Loading from an INI file
------------------------

``Configuration`` provider can load configuration from an ``ini`` file using the
:py:meth:`Configuration.from_ini` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_ini.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12

where ``examples/providers/configuration/config.ini`` is:

.. literalinclude:: ../../examples/providers/configuration/config.ini
   :language: ini

Alternatively, you can provide a path to the INI file over the configuration provider argument. In that case,
the container will call ``config.from_ini()`` automatically:

.. code-block:: python
   :emphasize-lines: 3

   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(ini_files=["./config.ini"])


   if __name__ == "__main__":
       container = Container()  # Config is loaded from ./config.ini


:py:meth:`Configuration.from_ini` method supports environment variables interpolation.

.. code-block:: ini

   [section]
   option1 = ${ENV_VAR}
   option2 = ${ENV_VAR}/path
   option3 = ${ENV_VAR:default}

See also: :ref:`configuration-envs-interpolation`.

Loading from a YAML file
------------------------

``Configuration`` provider can load configuration from a ``yaml`` file using the
:py:meth:`Configuration.from_yaml` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_yaml.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12

where ``examples/providers/configuration/config.yml`` is:

.. literalinclude:: ../../examples/providers/configuration/config.yml
   :language: ini

Alternatively, you can provide a path to the YAML file over the configuration provider argument. In that case,
the container will call ``config.from_yaml()`` automatically:

.. code-block:: python
   :emphasize-lines: 3

   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(yaml_files=["./config.yml"])


   if __name__ == "__main__":
       container = Container()  # Config is loaded from ./config.yml

:py:meth:`Configuration.from_yaml` method supports environment variables interpolation.

.. code-block:: ini

   section:
     option1: ${ENV_VAR}
     option2: ${ENV_VAR}/path
     option3: ${ENV_VAR:default}

See also: :ref:`configuration-envs-interpolation`.

:py:meth:`Configuration.from_yaml` method uses custom version of ``yaml.SafeLoader``.
To use another loader use ``loader`` argument:

.. code-block:: python

   import yaml


   container.config.from_yaml("config.yml", loader=yaml.UnsafeLoader)

.. note::

   Loading of a yaml configuration requires ``PyYAML`` package.

   You can install the ``Dependency Injector`` with an extra dependency::

      pip install dependency-injector[yaml]

   or install ``PyYAML`` directly::

      pip install pyyaml

   *Don't forget to mirror the changes in the requirements file.*

Loading from a JSON file
------------------------

``Configuration`` provider can load configuration from a ``json`` file using the
:py:meth:`Configuration.from_json` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_json.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12

where ``examples/providers/configuration/config.json`` is:

.. literalinclude:: ../../examples/providers/configuration/config.json
   :language: json

Alternatively, you can provide a path to a json file over the configuration provider argument. In that case,
the container will call ``config.from_json()`` automatically:

.. code-block:: python
   :emphasize-lines: 3

   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(json_files=["./config.json"])


   if __name__ == "__main__":
       container = Container()  # Config is loaded from ./config.json

:py:meth:`Configuration.from_json` method supports environment variables interpolation.

.. code-block:: json

   {
       "section": {
           "option1": "${ENV_VAR}",
           "option2": "${ENV_VAR}/path",
           "option3": "${ENV_VAR:default}"
       }
   }

See also: :ref:`configuration-envs-interpolation`.

Loading from a Pydantic settings
--------------------------------

``Configuration`` provider can load configuration from a ``pydantic_settings.BaseSettings`` object using the
:py:meth:`Configuration.from_pydantic` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_pydantic.py
   :language: python
   :lines: 3-
   :emphasize-lines: 32

To get the data from pydantic settings ``Configuration`` provider calls its ``model_dump()`` method.
If you need to pass an argument to this call, use ``.from_pydantic()`` keyword arguments.

.. code-block:: python

   container.config.from_pydantic(Settings(), exclude={"optional"})

Alternatively, you can provide a ``pydantic_settings.BaseSettings`` object over the configuration provider argument. In that case,
the container will call ``config.from_pydantic()`` automatically:

.. code-block:: python
   :emphasize-lines: 3

   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(pydantic_settings=[Settings()])


   if __name__ == "__main__":
       container = Container()  # Config is loaded from Settings()


.. note::

   ``Dependency Injector`` doesn't install ``pydantic-settings`` by default.

   You can install the ``Dependency Injector`` with an extra dependency::

      pip install dependency-injector[pydantic2]

   or install ``pydantic-settings`` directly::

      pip install pydantic-settings

   *Don't forget to mirror the changes in the requirements file.*

.. note::

   For backward-compatibility, Pydantic v1 is still supported.
   Passing ``pydantic.BaseSettings`` instances will work just as fine as ``pydantic_settings.BaseSettings``.

Loading from a dictionary
-------------------------

``Configuration`` provider can load configuration from a Python ``dict`` using the
:py:meth:`Configuration.from_dict` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_dict.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12-19

Loading from an environment variable
------------------------------------

``Configuration`` provider can load configuration from an environment variable using the
:py:meth:`Configuration.from_env` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_env.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18-20

You can use ``as_`` argument for the type casting of an environment variable value:

.. code-block:: python
   :emphasize-lines: 2,6,10

   # API_KEY=secret
   container.config.api_key.from_env("API_KEY", as_=str, required=True)
   assert container.config.api_key() == "secret"

   # SAMPLING_RATIO=0.5
   container.config.sampling.from_env("SAMPLING_RATIO", as_=float, required=True)
   assert container.config.sampling() == 0.5

   # TIMEOUT undefined, default is used
   container.config.timeout.from_env("TIMEOUT", as_=int, default=5)
   assert container.config.timeout() == 5


Loading a value
---------------

``Configuration`` provider can load configuration value using the
:py:meth:`Configuration.from_value` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_value.py
   :language: python
   :lines: 3-
   :emphasize-lines: 14-15

Loading from the multiple sources
---------------------------------

``Configuration`` provider can load configuration from the multiple sources. Loaded
configuration is merged recursively over the existing configuration.

.. literalinclude:: ../../examples/providers/configuration/configuration_multiple.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12-13

where ``examples/providers/configuration/config.local.yml`` is:

.. literalinclude:: ../../examples/providers/configuration/config.local.yml
   :language: ini

.. _configuration-envs-interpolation:

Using environment variables in configuration files
--------------------------------------------------

``Configuration`` provider supports environment variables interpolation in configuration files.
Use ``${ENV_NAME}`` in the configuration file to substitute value from environment
variable ``ENV_NAME``.

.. code-block:: ini

   section:
     option: ${ENV_NAME}

You can also specify a default value using ``${ENV_NAME:default}`` format. If environment
variable ``ENV_NAME`` is undefined, configuration provider will substitute value ``default``.

.. code-block:: ini

   [section]
   option = ${ENV_NAME:default}

If you'd like to specify a default value for environment variable inside of the application you can use
``os.environ.setdefault()``.

.. literalinclude:: ../../examples/providers/configuration/configuration_env_interpolation_os_default.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12

If environment variable is undefined and doesn't have a default, ``Configuration`` provider
will replace it with an empty value. This is a default behavior. To raise an error on
undefined environment variable that doesn't have a default value, pass argument
``envs_required=True`` to a configuration reading method:

.. code-block:: python

   container.config.from_yaml("config.yml", envs_required=True)

See also: :ref:`configuration-strict-mode`.

.. note::
   ``Configuration`` provider makes environment variables interpolation before parsing. This preserves
   original parser behavior. For instance, undefined environment variable in YAML configuration file
   will be replaced with an empty value and then YAML parser will load the file.

   Original configuration file:

   .. code-block:: ini

      section:
        option: ${ENV_NAME}

   Configuration file after interpolation where ``ENV_NAME`` is undefined:

   .. code-block:: ini

      section:
        option:

   Configuration provider after parsing interpolated YAML file contains ``None`` in
   option ``section.option``:

   .. code-block:: python

      assert container.config.section.option() is None

Mandatory and optional sources
------------------------------

By default, methods ``.from_yaml()`` and ``.from_ini()`` ignore errors if configuration file does not exist.
You can use this to specify optional configuration files.

If configuration file is mandatory, use ``required`` argument. Configuration provider will raise an error
if required file does not exist.

You can also use ``required`` argument when loading configuration from dictionaries and environment variables.

Mandatory YAML file:

.. code-block:: python

   container.config.from_yaml("config.yaml", required=True)

Mandatory INI file:

.. code-block:: python

   container.config.from_ini("config.ini", required=True)

Mandatory dictionary:

.. code-block:: python

   container.config.from_dict(config_dict, required=True)

Mandatory environment variable:

.. code-block:: python

   container.config.api_key.from_env("API_KEY", required=True)

See also: :ref:`configuration-strict-mode`.

Specifying the value type
-------------------------

You can specify the type of the injected configuration value explicitly.

This helps when you read the value from an ini file or an environment variable and need to
convert it into an ``int`` or a ``float``.

.. literalinclude:: ../../examples/providers/configuration/configuration_type.py
   :language: python
   :lines: 3-
   :emphasize-lines: 19

``Configuration`` provider has next helper methods:

- ``.as_int()``
- ``.as_float()``
- ``.as_(callback, *args, **kwargs)``

The last method ``.as_(callback, *args, **kwargs)`` helps to implement other conversions.

.. literalinclude:: ../../examples/providers/configuration/configuration_type_custom.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18

With the ``.as_(callback, *args, **kwargs)`` you can specify a function that will be called
before the injection. The value from the config will be passed as a first argument. The returned
value will be injected. Parameters ``*args`` and ``**kwargs`` are handled as any other injections.

.. _configuration-strict-mode:

Strict mode and required options
--------------------------------

You can use configuration provider in strict mode. In strict mode configuration provider raises an error
on access to any undefined option.

.. literalinclude:: ../../examples/providers/configuration/configuration_strict.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12

Methods ``.from_*()`` in strict mode raise an exception if configuration file does not exist or
configuration data is undefined:

.. code-block:: python
   :emphasize-lines: 10,15,20,25,30

   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(strict=True)


   if __name__ == "__main__":
       container = Container()

       try:
           container.config.from_yaml("does-not_exist.yml")  # raise exception
       except FileNotFoundError:
           ...

       try:
           container.config.from_ini("does-not_exist.ini")  # raise exception
       except FileNotFoundError:
           ...

       try:
           container.config.from_pydantic(EmptySettings())  # raise exception
       except ValueError:
           ...

       try:
           container.config.from_env("UNDEFINED_ENV_VAR")  # raise exception
       except ValueError:
           ...

       try:
           container.config.from_dict({})  # raise exception
       except ValueError:
           ...

Environment variables interpolation in strict mode raises an exception when encounters
an undefined environment variable without a default value.

.. code-block:: ini

   section:
     option: ${UNDEFINED}

.. code-block:: python

       try:
           container.config.from_yaml("undefined_env.yml")  # raise exception
       except ValueError:
           ...

You can override ``.from_*()`` methods behaviour in strict mode using ``required`` argument:

.. code-block:: python

   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(strict=True)


   if __name__ == "__main__":
       container = Container()

       container.config.from_yaml("config.yml")
       container.config.from_yaml("config.local.yml", required=False)

You can also use ``.required()`` option modifier when making an injection. It does not require to switch
configuration provider to strict mode.

.. literalinclude:: ../../examples/providers/configuration/configuration_required.py
   :language: python
   :lines: 11-20
   :emphasize-lines: 8-9

.. note::

   Modifier ``.required()`` should be specified before type modifier ``.as_*()``.

Aliases
-------

You can use ``Configuration`` provider with a context manager to create aliases.

.. literalinclude:: ../../examples/providers/configuration/configuration_alias.py
   :language: python
   :lines: 3-
   :emphasize-lines: 14,22

.. note::

   Library ``environs`` is a 3rd party library. You need to install it
   separately::

      pip install environs

   Documentation is available on GitHub: https://github.com/sloria/environs

Injecting invariants
--------------------

You can inject invariant configuration options based on the value of the other configuration
option.

To use that you should provide the switch-value as an item of the configuration option that
contains sections ``config.options[config.switch]``:

- When the value of the ``config.switch`` is ``A``, the ``config.options.A`` is injected
- When the value of the ``config.switch`` is ``B``, the ``config.options.B`` is injected

.. literalinclude:: ../../examples/providers/configuration/configuration_itemselector.py
   :language: python
   :lines: 3-
   :emphasize-lines: 15,30-31,38

.. disqus::
