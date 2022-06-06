"""
Scripts loading a static HTML site or CMS DB tables into MD files

>>> from page.imports import load_folder
>>> load_folder('./books/*.html', 'Books')
"""

import glob
import html
import os
from datetime import datetime

from django.template.defaultfilters import slugify
from lxml.html import fromstring, tostring
from markdownify import markdownify
from sqlalchemy import create_engine

SQL_CONNECT = "postgresql://user:password@host/database"
SQL_SELECT_SATCHMO = f"""
    SELECT p.id, p.name, p.slug, cc.slug AS parent,
           p.description, p.short_description, p.date_added
    FROM product_product AS p
    INNER JOIN product_product_category AS c
        ON p.id = c.product_id
    INNER JOIN product_category AS cc
        ON c.category_id = cc.id
    ORDER BY parent;"""
SQL_SELECT_WORDPRESS = f"""TBC"""

MD_ROOT = 'md/'


def load_folder(path, md_root=MD_ROOT):
    ls = glob.glob(path)
    for path in ls:
        load_path(path, md_root)


def load_db(query=SQL_SELECT_SATCHMO, md_root=MD_ROOT):
    """Export all to markdown"""
    os.makedirs(md_root)
    engine = create_engine(SQL_CONNECT)
    with engine.connect() as con:
        rs = con.execute(query)
        for row in rs:
            page = row
            save_md_page(page, md_root)


def load_path(path, md_root):
    fn = path.split('/')[-1]
    if fn.startswith('_') or fn == 'index.html':
        return
    doc = fromstring(open(path).read())
    title = doc.cssselect('h1')[0].text_content()
    author = doc.cssselect('.author b')[0].text_content()

    body = doc.cssselect('body')[0]
    for x in body.cssselect('.author') + body.cssselect('h1'):
        x.drop_tree()
    body = tostring(body).decode('utf-8').replace('<body>', '').replace('</body>', '').strip()
    body = html.unescape(body)
    slug = title.split(':')[0].lower().replace(' the ', ' ').replace(' a ', ' ')
    slug = ' '.join(slug.split()[:5])
    slug = slugify(slug).replace('-', '')
    page = dict(title=title, body=body, author=author, slug=slug)
    save_md_page(page, md_root)


def save_md_page(pd, md_root):
    """Exports a page dict pd as markdown file
    >>> p = dict(title='My title', slug='my_slug', parent='parent',
    >>>          body='Lorem ipsum...', children=True)
    >>> save_md_page(p, 'src')
    """
    title = pd.get('title')
    slug = pd.get('slug')
    parent = pd.get('parent')
    content = pd.get('body')
    author = pd.get('author', '')
    created = pd.get('created') or datetime.now()

    path = os.path.join(md_root, f'{slug}.txt')

    d = None  # subdirectory
    if parent:
        d = os.path.join(md_root, parent)
    if pd.get('children'):
        d = os.path.join(md_root, slug)
        path = path.replace('.md', '/index.md')
    if d and not os.path.exists(d + '/'):
        os.makedirs(d)
    with open(path, 'a+') as f:
        headline = f'{title}\n{"=" * len(title)}\n\n'
        author = f'By **{author}**\n\n' if author else ''
        body = markdownify(content, wrap=True)
        f.write(f"{headline}{author}{body}")
        f.close()
        ctime = created.timestamp()
        os.utime(path, (ctime, ctime))
