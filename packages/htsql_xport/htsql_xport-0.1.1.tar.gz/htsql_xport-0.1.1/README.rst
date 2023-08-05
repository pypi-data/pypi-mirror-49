********************
HTSQL_XPORT Overview
********************

The ``htsql_xport`` package is an extension for `HTSQL`_ that adds basic
support for SAS V5 XPORT transfer files.

.. _`HTSQL`: http://htsql.org/


Installation
============

Install this package like you would any other Python package::

    $ pip install htsql_xport


Add extension in your settings.yaml file::

    htsql_extensions:
        htsql_xport:

Or::

    mart_htsql_extensions:
        htsql_xport:

Formatters
==========

This extension adds a formatter function to HTSQL: ``/:xpt``.
It will output the results in SAS V5 XPORT transfer file format. 

