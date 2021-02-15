.. _check-container-dependencies:

Check container dependencies
----------------------------

To check container dependencies use method ``.check_dependencies()``.

.. literalinclude:: ../../examples/containers/check_dependencies.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12

Method ``.check_dependencies()`` raises an error if container has any undefined dependencies.
If all dependencies are provided or have defaults, no error is raised.

See also: :ref:`dependency-provider`.

.. disqus::
