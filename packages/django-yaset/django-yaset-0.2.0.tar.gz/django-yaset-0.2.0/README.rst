django-yaset
************

Yet Another Settings tool for django contains helper functions for managing
localized settings files for different deployments and developers.

Installation
============

.. code-block:: bash

    $ pip install django-yaset

Usage
=====

A common pattern in django to use different settings for different
environments is to have a "local_settings" directory. This utility makes this
easier. 

The expected directory setup is as follows:

.. code-block:: text

    project/
        settings.py
        local_settings/
            __init__.py
            import_redirect
            development.py
            production.py
            secrets/
                __init__.py
                development.py
                production.py
                

The ``import_redirect`` file should contain the local module name of the
settings to import in this environment. In the above example, it would be
either "development" or "production". The "devleopment" and "production" files
would contain the same types of declarations found in ``settings.py``.

Inside of your ``settings.py`` file, include this at the bottom:

.. code-block:: python

    from yaset import import_settings

    import_settings(globals())

This passes the ``settings`` packaging into the ``import_settings`` call which
loads ``import_redirect``, uses its contents to then load the
``local_settings`` and ``local_settings.secrets`` files specified. 

It is not generally recommended to put either the ``import_redirect`` file or
the ``secrets`` directory in your repository.


Supports
========

django-yaset has been tested with:

* Django 2.2.3 using Python 3.6, 3.7

Docs & Source
=============

Docs: http://django-yaset.readthedocs.io/en/latest/

Source: https://github.com/cltrudeau/django-yaset
