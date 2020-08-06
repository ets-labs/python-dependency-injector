Asyncio daemon tutorial
=======================

.. _asyncio-daemon-tutorial:

This tutorials shows how to build an ``asyncio`` daemon following the dependency injection
principle.

Start from the scratch or jump to the section:

.. contents::
   :local:
   :backlinks: none

You can find complete project on the
`Github <https://github.com/ets-labs/python-dependency-injector/tree/master/examples/miniapps/monitoring-daemon-asyncio>`_.

What are we going to build?
---------------------------

We will build a monitoring daemon that monitors web services availability.

The daemon will send the requests to the `example.com <http://example.com>`_ and
`httpbin.org <https://httpbin.org>`_ every couple of seconds. For each successfully completed
response it will log:

- The response code
- The amount of bytes in the response
- The time took to complete the response

.. image::  asyncio_images/diagram.png

Prepare the environment
-----------------------

Project layout
--------------

Install the requirements
------------------------

Minimal application
-------------------

HTTP monitor
------------

Add another monitor
-------------------

Tests
-----

Conclusion
----------

.. disqus::
