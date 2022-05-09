"""
Test scripts loading a clean flat static HTML site into
legacy pages DB records and exporting the records back to a set of markdown files

>>> from page.tests import load_folder
>>> load_folder('./books/*.html', 'Books')
"""

import glob
import html
import os
from unittest import TestCase

from django.template.defaultfilters import slugify
from lxml.html import fromstring, tostring
from markdownify import markdownify

from page.models import Page


def load_folder(path, title):
    ls = glob.glob(path)
    parent = Page(title=title, body='***')
    parent.save()
    for path in ls:
        load_path(path, parent)


def load_path(path, parent):
    fn = path.split('/')[-1]
    if fn.startswith('_') or fn == 'index.html':
        return
    doc = fromstring(open(path).read())
    title = doc.cssselect('h1')[0].text_content()
    author = doc.cssselect('.author b')[0].text_content()
    try:
        asin = doc.cssselect('a')[0].get('href').split(';')[0].split(':')[1]
    except IndexError:
        asin = ''
    body = doc.cssselect('body')[0]
    for x in body.cssselect('.author') + body.cssselect('h1'):
        x.drop_tree()
    body = tostring(body).decode('utf-8').replace('<body>', '').replace('</body>', '').strip()
    body = html.unescape(body)
    slug = title.split(':')[0].lower().replace(' the ', ' ').replace(' a ', ' ')
    slug = ' '.join(slug.split()[:5])
    slug = slugify(slug).replace('-', '')
    if asin:
        slug = f'{slug}_{asin}'
    p = Page(title=title, body=body, author=author, slug=slug, parent=parent, active=True)
    p.save()


def export_md_page(page, md_root):
    """Exports a page as markdown file"""
    path = os.path.join(md_root, page.get_absolute_url()[1:] + '.md')
    d = None  # subdirectory
    if page.parent:
        d = os.path.join(md_root, page.parent.slug)
    if page.children():
        d = os.path.join(md_root, page.slug)
        path = path.replace('.md', '/index.md')
    if d and not os.path.exists(d + '/'):
        os.makedirs(d)
    with open(path, 'a+') as f:
        headline = f'{page.title}\n{"=" * len(page.title)}\n\n'
        author = f'By **{page.author}**\n\n' if page.author else ''
        body = markdownify(page.body, wrap=True)
        f.write(f"{headline}{author}{body}")
        f.close()
        ctime = page.created.timestamp()
        os.utime(path, (ctime, ctime))


def export_md(md_root='md/'):
    """Export all to markdown"""
    os.makedirs(md_root)
    for page in Page.objects.all():
        export_md_page(page, md_root)


class PageTestCase(TestCase):
    def test_model(self):
        """Test a page"""
        p = Page(body='Lorem ipsum...', title='My title', slug='my-title')
        self.assertEqual(p.slug, 'my-title')
        self.assertEqual(p.title, 'My title')
