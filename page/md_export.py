"""Export all pages to markdown"""

import os
from markdownify import markdownify
from page.models import Page

EXPORT_DIR = 'mdpages/'


def export_page(p):
    path = EXPORT_DIR + p.get_absolute_url()[1:] + '.md'
    d = None  # subdirectory
    if p.parent:
        d = EXPORT_DIR + p.parent.slug
    if p.children():
        d = EXPORT_DIR + p.slug
        path = path.replace('.md', '/index.md')
    if d and not os.path.exists(d + '/'):
        os.makedirs(d)
    with open(path, 'a+') as f:
        f.write(p.title)
        f.write(f"\n{'='*len(p.title)}\n")
        f.write(markdownify(p.body))
        f.close()
        ctime = p.created_at.timestamp()
        os.utime(path, (ctime, ctime))


os.makedirs(EXPORT_DIR)
for p in Page.objects.all():
    export_page(p)
