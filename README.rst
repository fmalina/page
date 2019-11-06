Simple page and redirect management.

- parent -> child organizable pages
- redirects with usage tracking


Installation (into a Django project)
------------------------------------

To get the latest version from GitHub

::

    pip3 install -e git+git://github.com/fmalina/django-page.git#egg=page

Add ``page`` to your ``INSTALLED_APPS``

.. code:: python

    INSTALLED_APPS = (
        ...,
        'page',
    )

Configure your settings to suit, see page/app_settings.py.

Add the ``page`` URLs to your ``urls.py``

.. code:: python

    urlpatterns = [
        ...
        path('', include('page.urls')),
    ]

Add middleware and adjust settings:

.. code:: python

    MIDDLEWARE += [
        'page.middleware.fallback_middleware'
    ]

    # APPEND_SLASH must be off
    APPEND_SLASH = False

    # SITE_URL also needs to be in your generic context as {{ site_url }}
    # add it to your context processor if you didn't yet
    SITE_URL = 'https://example.org'


Create your tables

::

    ./manage.py migrate page
