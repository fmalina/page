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

Create your tables

::

    ./manage.py migrate page
