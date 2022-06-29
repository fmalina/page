"""
Static cache utilities for use with Django sites
Provided here but not used in *Page*, which does not require Django.

Pages middleware and view decorator to speed up many parts of Django apps.

With `'page.static.static_cache_middleware'` added to middleware settings
and `CACHING = True` one can export static "detail" pages like so:

   from page.static import static_cache

   @static_cache
   def my_model_detail_view(request, pk):
       ...
"""

from functools import wraps
from page.gen import write_content


def static_cache_middleware(get_response):
    """Django static file generating middleware."""
    from django.conf import settings

    def middleware(request):
        response = get_response(request)
        static_gen = response.get('Static-Cache', False)
        if static_gen:
            del response['Static-Cache']
        if settings.CACHING and response.status_code == 200 and static_gen:
            write_content(
                settings.STATIC_ROOT,
                request.get_full_path(),
                response.content
            )
        return response

    return middleware


def static_cache(view_func):
    """Django view decorator that adds key to a response
    so that it will be static cached."""

    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Static-Cache'] = True
        return response

    return _wrapped_view_func
