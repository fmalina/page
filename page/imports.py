#!/usr/bin/env python3
"""
Load a CMS database into .md text files
=======================================
Connects to CMS DB using env. variables,
selects columns for pages (see PAGE_COLS), saves markdown.

Use DB_NAME, DB_USER, DB_PASS ... env vars, or specify DB_URI.
Use DB_QUERY that spits out PAGE_COLS. Example WordPress query is provided.
Send a PR with your query in the collection CMS_QUERIES.

$ export DB_NAME=...DB_USER, DB_PASS, ...CMS_NAME
$ # or export DB_URI=postgres..., DB_QUERY
$ ./page/imports.py

Convert a static HTML site into source text files
-------------------------------------------------
To load Markdown from existing static site, use Python terminal.
Using load_path as an example with all the tricks, hack your HTML parsing fuction.

>>> from page.imports import load_folder, load_path
>>> # def load_path()... # override load path as needed
>>> load_folder('./books/*.html', 'Books', load_func=load_path)
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
DB_HOST = os.getenv('DB_HOST') or 'localhost'
CMS_NAME = os.getenv('CMS_NAME') or 'wordpress'
DB_URI = os.getenv('DB_URI') or f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
PAGE_COLS = ['id', 'title', 'slug', 'parent', 'body', 'desc', 'created']
CMS_QUERIES = {
    'wordpress': f"""
        SELECT p.ID, p.post_title, p.post_name, par.post_name AS parent,
               p.post_content, p.post_excerpt, p.post_date
        FROM wp_posts AS p
        INNER JOIN wp_posts AS par
            ON p.post_parent = par.ID
        ORDER BY parent;""",
    'satchmo': f"""
        SELECT p.id, p.name, p.slug, cc.slug AS parent,
               p.description, p.short_description, p.date_added
        FROM product_product AS p
        INNER JOIN product_product_category AS c
            ON p.id = c.product_id
        INNER JOIN product_category AS cc
            ON c.category_id = cc.id
        ORDER BY parent;""",
    # add a SELECT query for your CMS that returns PAGE_COLS data
    # ...
}
MD_ROOT = 'md/'


def load_db(md_root=MD_ROOT):
    """Export all DB rows to markdown text files"""
    if not os.path.exists(md_root):
        os.makedirs(md_root)
    engine = create_engine(DB_URI)
    with engine.connect() as con:
        query = os.getenv('DB_QUERY') or CMS_QUERIES[CMS_NAME]
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


def load_folder(path, md_root=MD_ROOT, load_func=load_path):
    ls = glob.glob(path)
    for path in ls:
        load_func(path, md_root)


def save_md_page(pd, md_root):
    """
    Exports a page dict pd as markdown file
    >>> p = dict(title='My title', slug='my_slug', parent='parent',
    >>>          body='Lorem ipsum...', children=True)
    >>> save_md_page(p, 'src')
    """
    title = pd.get('title')
    slug = pd.get('slug')
    parent = pd.get('parent', '')
    content = pd.get('body')
    author = pd.get('author', '')
    created = pd.get('created') or date.today()
    created = datetime.combine(created, datetime.min.time())

    path = os.path.join(md_root, parent, f'{slug}.md')
    d = os.path.join(md_root, parent)
    if parent == '':
        d = os.path.join(md_root, slug)
        path = os.path.join(md_root, f'{slug}/index.md')
    if not os.path.exists(d):
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
    load_db()
