prettylog
=========

.. image:: https://coveralls.io/repos/github/mosquito/prettylog/badge.svg?branch=master
    :target: https://coveralls.io/github/mosquito/prettylog
    :alt: Coveralls

.. image:: https://travis-ci.org/mosquito/prettylog.svg
    :target: https://travis-ci.org/mosquito/prettylog
    :alt: Travis CI

.. image:: https://img.shields.io/pypi/v/prettylog.svg
    :target: https://pypi.python.org/pypi/prettylog/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/wheel/prettylog.svg
    :target: https://pypi.python.org/pypi/prettylog/

.. image:: https://img.shields.io/pypi/pyversions/prettylog.svg
    :target: https://pypi.python.org/pypi/prettylog/

.. image:: https://img.shields.io/pypi/l/prettylog.svg
    :target: https://pypi.python.org/pypi/prettylog/

Let's write beautiful logs:

.. code-block:: python

    import logging
    from prettylog import basic_config


    # Configure logging
    basic_config(level=logging.INFO, buffered=False, log_format='color')


Available formats
-----------------

* stream - default behaviour
* color - colored logs
* json - json representation
* syslog - writes to syslog

Quick start
-----------

Setting up json logs:

.. code-block:: python

    import logging
    from prettylog import basic_config


    # Configure logging
    basic_config(level=logging.INFO, buffered=False, log_format='json')


Buffered log handler
++++++++++++++++++++

Parameter `buffered=True` enables memory buffer which flushing logs delayed.

.. code-block:: python

    import logging
    from prettylog import basic_config

    basic_config(
        level=logging.INFO,
        buffered=True,
        buffer_size=10,             # flush each 10 log records
        flush_level=loggging.ERROR, # or when record with this level will be sent
        log_format='color',
        date_format=None,           # Disable date for logs, True enables it.
                                    # str with format is custom date format.
    )
