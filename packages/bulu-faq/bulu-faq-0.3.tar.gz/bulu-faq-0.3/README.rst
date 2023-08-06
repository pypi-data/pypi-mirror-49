Bulu FAQ
========

Stupid simple FAQ app to use with any django project. Includes admin definitions and a read-only API using Django Rest Framework.

Installation
------------

Install using pip::

    pip install bulu-faq


Configuration
-------------

Add ``faq`` to your installed apps in ``settings.py``::

    INSTALLED_APPS = (
        ...
        'faq',
    )

Add the urls in ``urls.py``::

    urlpatterns = [
        ...
        path('faq/', include('faq.urls'))
    ]
