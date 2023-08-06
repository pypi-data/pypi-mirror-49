========
date-cli
========

.. image:: https://travis-ci.org/Jhengsh/date-cli.svg?branch=master
   :target: https://travis-ci.org/Jhengsh/date-cli
   :alt: Build Status

This package provides date command line.

* date_range: help you generate date between 2 date(format: yyyymmdd)

------------
Installation
------------

The easiest way to install date-cli is to use `pip` in a ``virtualenv``::

    $ pip install git+https://github.com/Jhengsh/date-cli.git

--------
Tuturial
--------

Basic Use::

    $ date_range -s 20200225 -e 20200305 | awk '{print "python execute.py --yyyymmdd "$1";"}'
    # python execute.py --yyyymmdd 20200225;
    # python execute.py --yyyymmdd 20200226;
    # python execute.py --yyyymmdd 20200227;
    # python execute.py --yyyymmdd 20200228;
    # python execute.py --yyyymmdd 20200229;
    # python execute.py --yyyymmdd 20200301;
    # python execute.py --yyyymmdd 20200302;
    # python execute.py --yyyymmdd 20200303;
    # python execute.py --yyyymmdd 20200304;
    # python execute.py --yyyymmdd 20200305;
