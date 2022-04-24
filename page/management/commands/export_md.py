"""Export all pages to markdown"""

import os

from django.conf import settings
from django.core.management.base import BaseCommand
from markdownify import markdownify

from page.models import Page

MD_ROOT = settings.MD_ROOT


def export_page(page):
    """Exports a page p as markdown file"""
    path = os.path.join(MD_ROOT, page.get_absolute_url()[1:] + '.md')
    d = None  # subdirectory
    if page.parent:
        d = os.path.join(MD_ROOT, page.parent.slug)
    if page.children():
        d = os.path.join(MD_ROOT, page.slug)
        path = path.replace('.md', '/index.md')
    if d and not os.path.exists(d + '/'):
        os.makedirs(d)
    with open(path, 'a+') as f:
        f.write(page.title)
        f.write(f"\n{'='*len(page.title)}\n")
        f.write(markdownify(page.body, wrap=True))
        f.close()
        ctime = page.created_at.timestamp()
        os.utime(path, (ctime, ctime))


class Command(BaseCommand):
    def handle(self, *args, **options):
        os.makedirs(MD_ROOT)
        for page in Page.objects.all():
            export_page(page)
