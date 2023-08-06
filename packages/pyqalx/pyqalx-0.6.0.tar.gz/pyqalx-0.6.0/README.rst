pyqalx
======

Interfaces to qalx. For more details, see `project documentation, <http://docs.qalx.io>`_.

.. admonition:: development status

   ``pyqalx`` is currently under active development. It is pre-version 1.0 beta software and so each minor version
   can introduce breaking changes.

**qalx** (an abbreviation of "queued calculations" and pronounced "kal-x") is a flexible data management platform for engineering projects. Users store data and files in qalx and it provides tools for passing that data between various systems for processing.

There will eventually be four ways to interact with the platform:

-  A Python interface (pyqalx)
-  REST API (api.qalx.io)
-  Web console (qalx.io) - coming soon
-  A command line interface (qalx-cli) - coming soon

Most users are expected to use the web console and either the python or
command line interfaces. The REST API is intended to be used if you
prefer to access the platform with a language other than Python or want
to create a custom interface.

.. _installing:

Installing
==========

**qalx** is written in `Python <https://python.org>`_ and can be
installed via the Python Package Index (PyPi) with:

.. code:: bash

   pip install pyqalx

If installation has completed properly you should be able to import
``pyqalx`` in a python console:

>>> import pyqalx

.. warning::

      pyqalx requires **Python versions above 3.6**.


Configuration and Authentication
--------------------------------

Everything you do with **qalx** requires you to be authenticated. That
is, the platform requires you to identify yourself and will record all
your actions as being performed by you.

The way that **qalx** knows who you are is by reading a ``TOKEN``
which must be sent with every request.

.. warning::
   During this beta phase, you have to request a ``TOKEN`` by registering your interest at `qalx.io <https://qalx.io>`_

The easiest way to make sure that your token is sent with every request is to make sure you have a valid ``.qalx`` file
saved in your HOME directory.

.. admonition::  where is ``HOME``?

   The ``HOME`` directory can usually be found by putting %USERPROFILE%
   in the address bar in Windows Explorer or it is simply ``~`` on unix
   systems.

Adding the ``TOKEN`` to your config file under the default profile will ensure automatic
authentication.

.. code:: ini

   [default]
   TOKEN = 632gd7yb9squd0q8sdhq0s8diqsd0nqsdq9sdj

Any other configuration settings can be stored in the same file see `<https://docs.qalx.io/configuration>`_ for more information.

Quickstart
----------

The best place to get started: `<https://docs.qalx.io/quickstart>`_



