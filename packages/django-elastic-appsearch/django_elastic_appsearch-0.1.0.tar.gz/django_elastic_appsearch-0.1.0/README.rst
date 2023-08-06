=============================
Django Elastic App Search
=============================

.. image:: https://badge.fury.io/py/django_elastic_appsearch.svg
    :target: https://badge.fury.io/py/django_elastic_appsearch

.. image:: https://travis-ci.org/CorrosiveKid/django_elastic_appsearch.svg?branch=master
    :target: https://travis-ci.org/CorrosiveKid/django_elastic_appsearch

.. image:: https://codecov.io/gh/CorrosiveKid/django_elastic_appsearch/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/CorrosiveKid/django_elastic_appsearch

Integrate your Django Project with Elastic App Search with ease.

Documentation
-------------

The full documentation is at https://django_elastic_appsearch.readthedocs.io.

Quickstart
----------

Install Django Elastic App Search::

    pip install django_elastic_appsearch

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_elastic_appsearch',
        ...
    )

Add the Elastic App Search URL and Key to your settings module:

.. code-block:: python

    APPSEARCH_URL = 'https://appsearch.base.url'
    APPSEARCH_API_KEY = 'some_appsearch_api_token'

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
