=============================
acdh-django-netvis
=============================

.. image:: https://github.com/acdh-oeaw/acdh-django-netvis/actions/workflows/test.yml/badge.svg
    :target: https://github.com/acdh-oeaw/acdh-django-netvis/actions/workflows/test.yml

.. image:: https://github.com/acdh-oeaw/acdh-django-netvis/actions/workflows/build.yml/badge.svg
        :target: https://github.com/acdh-oeaw/acdh-django-netvis/actions/workflows/build.yml

.. image:: https://badge.fury.io/py/acdh-django-netvis.svg
    :target: https://badge.fury.io/py/acdh-django-netvis

.. image:: https://codecov.io/gh/acdh-oeaw/acdh-django-netvis/branch/master/graph/badge.svg?token=WP3PFBLX6V
    :target: https://codecov.io/gh/acdh-oeaw/acdh-django-netvis

.. image:: https://readthedocs.org/projects/acdh-django-netvis/badge/?version=latest
    :target: https://acdh-django-netvis.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
    

App to visualize model objects as network graph


Quickstart
----------

Install acdh-django-netvis::

    pip install acdh_django_netvis

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'netvis',
        ...
    )

Add acdh-django-netvis's URL patterns:

.. code-block:: python


    urlpatterns = [
        ...
        url(r'^netvis/', include('netvis.urls', namespace="netvis")),
        ...
    ]


Documentation
-------------


https://acdh-django-netvis.readthedocs.io.

Features
----------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ python manage.py test

Credits
----------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
