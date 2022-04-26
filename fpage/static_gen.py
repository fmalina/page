"""
Static site generator with static cache utilities for Django

>>> from fpage.static_gen import generate_site
>>> generate_site('blocl-pages', 'blocl/static/')
"""
import os
import shutil
from functools import wraps

import brotli

from fpage.models import Page
from fpage.views import render_feed, render_page


def generate_site(source_root, export_root):
    pages = Page.list(source_root, date_order=True)
    for p in pages:
        content = render_page(p).encode()
        generate_page(export_root, p.get_absolute_url(), content)
    feed = render_feed(pages).encode()
    generate_page(export_root, '/feed.xml', feed)


def generate_page(root, path, content):
    """Utility to write and brotli compress a page
    given a server root, URL path and page content"""
    no_leading_slash = str(path)[1:]
    full_path = os.path.join(root, no_leading_slash)
    if '/' in path[1:]:
        folder = os.path.join(root, *path.split('/')[1:-1])
        if not os.path.exists(folder):
            os.makedirs(folder)
    if path.endswith('/'):
        full_path = full_path + 'index.html'
    with open(full_path, 'wb+') as f:
        f.write(content)
    with open(full_path + '.br', 'wb+') as cf:
        compressed = brotli.compress(content)
        cf.write(compressed)


def static_gen_middleware(get_response):
    """Django static file generating middleware."""
    from django.conf import settings

    def middleware(request):
        response = get_response(request)
        static_gen = response.get('Static-Cache', False)
        if static_gen:
            del response['Static-Cache']
        if settings.CACHING and response.status_code == 200 and static_gen:
            generate_page(
                settings.STATIC_ROOT,
                request.get_full_path(),
                response.content
            )
        return response

    return middleware


def static_gen(view_func):
    """Django view decorator that adds key to a response
    so that it will be static cached."""

    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Static-Cache'] = True
        return response

    return _wrapped_view_func


# Cache clearing utils


def delete_folders(folders, root):
    """Delete static files caches for all sites used by."""
    for folder_name in folders:
        try:
            path = os.path.join(root, folder_name)
            shutil.rmtree(path, ignore_errors=True)
        except FileNotFoundError:
            pass


def delete_files(paths):
    """Delete files from a list of paths"""
    for path in paths:
        if os.path.exists(path):
            os.remove(path)
