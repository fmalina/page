import os
import shutil
from functools import wraps

import brotli
from django.conf import settings


def static_cache_middleware(get_response):
    """Static file caching middleware."""

    def middleware(request):
        response = get_response(request)

        try:
            root = settings.STATIC_ROOT
        except AttributeError:  # no segment on the request
            return response
        path = request.get_full_path()

        static_cache = response.get('Static-Cache', False)
        if static_cache:
            del response['Static-Cache']

        if settings.CACHING and response.status_code == 200 and static_cache:
            full_path = os.path.join(root, path[1:])
            if '/' in path[1:]:
                folder = os.path.join(root, *path.split('/')[1:-1])
                if not os.path.exists(folder):
                    os.makedirs(folder)
            if path.endswith('/'):
                full_path = full_path + 'index.html'
            with open(full_path, 'wb+') as f:
                f.write(response.content)
            with open(full_path + '.br', 'wb+') as cf:
                compressed = brotli.compress(response.content)
                cf.write(compressed)
        return response

    return middleware


def static_cache(view_func):
    """Decorator that adds key to a response so that it will
    be static cached."""

    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Static-Cache'] = True
        return response

    return _wrapped_view_func


def delete_related_cached(o, qs):
    """Delete cached page for object o and
    queryset qs of affected cached pages linking to it."""
    ls = list(qs) + [o]
    folder = settings.STATIC_ROOT
    for f in ls:
        path = folder + f.get_absolute_url()
        if os.path.exists(path):
            os.remove(path)


def delete_segment(name):
    path = settings.STATIC_ROOT + name + '/'
    try:
        shutil.rmtree(path, ignore_errors=True)
    except FileNotFoundError:
        pass


def reset_cache():
    """
    Delete static files caches for all sites used by.
    $ ./manage.py reset_cache
    """
    for name in settings.SEGMENTS:
        delete_segment(name)
