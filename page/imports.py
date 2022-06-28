#!/usr/bin/env python3
"""
Load a static HTML site or CMS database into MD files

>>> from page.imports import load_folder
>>> load_folder('./books/*.html', 'Books')
"""

import glob
import html
import os
from datetime import datetime, date

from django.template.defaultfilters import slugify
from lxml.html import fromstring, tostring
from markdownify import markdownify
from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

SQL_CONNECT = f"mysql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}"
SQL_SELECT_WP = f"""
    SELECT p.ID, p.post_title, p.post_name, par.post_name AS parent,
           p.post_content, p.post_excerpt, p.post_date
    FROM wp_posts AS p
    INNER JOIN wp_posts AS par
        ON p.post_parent = par.ID
    ORDER BY parent;"""
SQL_SELECT_SATCHMO = f"""
    SELECT p.id, p.name, p.slug, cc.slug AS parent,
           p.description, p.short_description, p.date_added
    FROM product_product AS p
    INNER JOIN product_product_category AS c
        ON p.id = c.product_id
    INNER JOIN product_category AS cc
        ON c.category_id = cc.id
    ORDER BY parent;"""

PAGE_COLS = ['id', 'name', 'title', 'parent',
             'body', 'meta', 'created']
MD_ROOT = 'md/'


def load_folder(path, md_root=MD_ROOT):
    ls = glob.glob(path)
    for path in ls:
        load_path(path, md_root)


def load_db(query=SQL_SELECT_WP, md_root=MD_ROOT):
    """Export all DB rows to markdown text files"""
    if not os.path.exists(md_root):
        os.makedirs(md_root)
    engine = create_engine(SQL_CONNECT)
    with engine.connect() as con:
        rs = con.execute(query)
        for row in rs:
            page = dict(zip(PAGE_COLS, row))
            save_md_page(page, md_root)


def load_path(path, md_root):
    """Parse a HTML file to page dict to save as .md"""
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
    """
    Exports a page dict pd as markdown file
    >>> p = dict(title='My title', slug='my_slug', parent='parent',
    >>>          body='Lorem ipsum...', children=True)
    >>> save_md_page(p, 'src')
    """
    title = pd.get('title')
    slug = pd.get('slug')
    parent = pd.get('parent')
    content = pd.get('body')
    author = pd.get('author', '')
    created = pd.get('created') or date.taday()
    created = datetime.combine(created, datetime.min.time())

    path = os.path.join(md_root, f'{slug}.md')

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


if __name__ == '__main__':
    # load_folder()
    load_db()
