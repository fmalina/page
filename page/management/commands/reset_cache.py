"""
Delete static file caches
./manage.py reset_cache
"""
import os

import django
from django.core.management.base import BaseCommand

from page.static_cache import reset_cache


def restore_symlinks():
    pth = django.__file__.split('django')[0]
    os.system(f'ln -s {pth}django/contrib/admin/static/admin static/static/admin')

    # if django-upload is installed
    up = f'{pth}upload/static/upload'
    if os.path.exists(up):
        os.system(f'ln -s {up} static/static/upload')


class Command(BaseCommand):
    def handle(self, *args, **options):
        reset_cache()
        restore_symlinks()
