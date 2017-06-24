+++
date = "2017-06-24T23:18:49+08:00"
tags = ["github","Python"]
title = "TinyDB - lightweight document oriented database for Python"

+++

> TinyDB is a lightweight document oriented database optimized for your happiness<!--more-->


**TinyDB** is written in pure Python and has no external dependencies. The target are
small apps that would be blown away by a SQL-DB or an external database server.

TinyDB is:

- **tiny:** The current source code has 1200 lines of code (with about 40%
  documentation) and 1000 lines tests. For comparison: Buzhug_ has about 2500
  lines of code (w/o tests), CodernityDB_ has about 7000 lines of code
  (w/o tests).

- **document oriented:** Like MongoDB_, you can store any document
  (represented as ``dict``) in TinyDB.

- **optimized for your happiness:** TinyDB is designed to be simple and
  fun to use by providing a simple and clean API.

- **written in pure Python:** TinyDB neither needs an external server (as
  e.g. `PyMongo <http://api.mongodb.org/python/current/>`_) nor any dependencies
  from PyPI.

- **works on Python 2.6 + 2.7 and 3.3 – 3.5 and PyPy:** TinyDB works on all
  modern versions of Python and PyPy.

- **powerfully extensible:** You can easily extend TinyDB by writing new
  storages or modify the behaviour of storages with Middlewares.

- **100% test coverage:** No explanation needed.

To dive straight into all the details, head over to the `TinyDB docs
<https://tinydb.readthedocs.io/>`_. You can also discuss everything related
to TinyDB like general development, extensions or showcase your TinyDB-based
projects on the `discussion forum <http://forum.m-siemens.de/.>`_.

---

Example Code
************

.. code-block:: python

    >>> from tinydb import TinyDB, Query
    >>> db = TinyDB('/path/to/db.json')
    >>> db.insert({'int': 1, 'char': 'a'})
    >>> db.insert({'int': 1, 'char': 'b'})

Query Language
==============

.. code-block:: python

    >>> User = Query()
    >>> # Search for a field value
    >>> db.search(User.name == 'John')
    [{'name': 'John', 'age': 22}, {'name': 'John', 'age': 37}]

    >>> # Combine two queries with logical and
    >>> db.search((User.name == 'John') & (User.age <= 30))
    [{'name': 'John', 'age': 22}]

    >>> # Combine two queries with logical or
    >>> db.search((User.name == 'John') | (User.name == 'Bob'))
    [{'name': 'John', 'age': 22}, {'name': 'John', 'age': 37}, {'name': 'Bob', 'age': 42}]

    >>> # More possible comparisons:  !=  <  >  <=  >=
    >>> # More possible checks: where(...).matches(regex), where(...).test(your_test_func)

Tables
======

.. code-block:: python

    >>> table = db.table('name')
    >>> table.insert({'value': True})
    >>> table.all()
    [{'value': True}]

Using Middlewares
=================

.. code-block:: python

    >>> from tinydb.storages import JSONStorage
    >>> from tinydb.middlewares import CachingMiddleware
    >>> db = TinyDB('/path/to/db.json', storage=CachingMiddleware(JSONStorage))


Supported Python Versions
*************************

TinyDB has been tested with Python 2.6, 2.7, 3.3 - 3.5 and PyPy.