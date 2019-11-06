"""
Example script loading a clean flat static HTML site into the CMS

>>> from page.static_loader import load_folder
>>> load_folder('/Users/f/PROJECTS/books/*.html', 'Books')

"""

import glob
import html

from django.template.defaultfilters import truncatewords, slugify
from lxml.html import fromstring, tostring

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
    slug = slugify(truncatewords(slug, 5))
    if asin:
        slug = f'{slug}.{asin}'
    p = Page(title=title, body=body, author=author, slug=slug, parent=parent, active=True)
    p.save()
