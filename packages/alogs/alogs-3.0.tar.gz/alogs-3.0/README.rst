Simple logging lib
==================

All code should use Python standard log module instead of ``print()``
function.

Install
-------

::

    python3 setup.py install

Usage
-----

Basic usage.

.. code:: python

    from alogs import get_logger

    logger = get_logger('module_name')

    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')

Log file
~~~~~~~~

Store logs into a file.

.. code:: python

    from alogs import get_logger

    logger = get_logger('module_name', 'log_file.log')

    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')

Disable existing loggers
~~~~~~~~~~~~~~~~~~~~~~~~

Prevent existing loggers to log.

.. code:: python

    from alogs import get_logger

    logger = get_logger('module_name', disable_existing_loggers=True)

    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')

Test
----

To test it just execute the ``test.py``:

::

    ~ python3 test.py

You should see:

::

    INFO 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_simple_logs() test.py:8 [logs] = Info simple message
    WARNING 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_simple_logs() test.py:9 [logs] = Warning simple message
    ERROR 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_simple_logs() test.py:10 [logs] = Error simple message
    CRITICAL 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_simple_logs() test.py:11 [logs] = Critical simple message
    INFO 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_module_name_logs() test.py:17 [module_name] = Info module message
    WARNING 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_module_name_logs() test.py:18 [module_name] = Warning module message
    ERROR 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_module_name_logs() test.py:19 [module_name] = Error module message
    CRITICAL 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_module_name_logs() test.py:20 [module_name] = Critical module message
    INFO 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_file_logs() test.py:26 [file_logs] = Info file message
    WARNING 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_file_logs() test.py:27 [file_logs] = Warning file message
    ERROR 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_file_logs() test.py:28 [file_logs] = Error file message
    CRITICAL 25/Jul/2019:11:17:06 -0300 MainProcess:4652 test:test_file_logs() test.py:29 [file_logs] = Critical file message

