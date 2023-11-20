+++
date = "2022-06-24T23:18:49+08:00"
tags = ["github","Python"]
title = "TinyDB - 一种轻量级的面向文档的Python数据库"

+++

> [TinyDB](https://github.com/msiemens/tinydb)是一个轻量级的面向文档的数据库，为您的幸福而优化<!--more-->


**TinyDB** 采用纯Python编写，没有外部依赖。祀标两者
小型应用程序会被SQL-DB或外部数据库服务器吹走。

TinyDB是：

- **tiny：** 目前的源代码有1200行代码（约占40%）。
文档）和1000行测试。相比之下：Buzhug_有大约2500个
行代码（无测试），CodernityDB_大约有7000行代码
（无测试）。

- **面向文档：** 和MongoDB_一样，可以存储任何文档
（表示为"dict"）。

- **为您的幸福而优化：** TinyDB设计简单，
通过提供一个简单而干净的API来有趣地使用。

- **纯Python编写：** TinyDB不需要外部服务器（如
例如`PyMongo <http://api.mongodb.org/python/current/>`_）也没有任何依赖关系
在PyPI

- **适用于Python 2.6 + 2.7和3.3 - 3.5以及PyPy：** TinyDB适用于所有
现代版本的Python和PyPy。

- **强大的可扩展性：** 您可以通过编写新的
存储或使用中间件修改存储的行为。

- **100%测试覆盖率：** 无需解释。

要深入了解所有细节，请转到`TinyDB文档<https://tinydb.readthedocs.io/>`。你也可以讨论一切有关
像TinyDB一般的开发，扩展或展示你的TinyDB的基础在“讨论论坛<http://forum.m-siemens.de/>”上的项目。

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