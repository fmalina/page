import json
import os
import shutil
from pathlib import Path

import brotli
import click
import jinja2
from jinja2 import Environment, PackageLoader, FileSystemLoader

from page.models import Page


@click.command("cli", context_settings={'show_default': True})
@click.option('--source', default='.', help='Source folder with markdown files')
@click.option('--target', default='_static', help='Destination folder for static site')
@click.option('--tpl', default='page', help='Custom template folder')
@click.option('--ext', default='.htm', help='File extension')
@click.option('--ctx', default='', help='Extra context')
def cli(source, target, tpl, ext, ctx):
    generate_site(source, target, tpl, ext, ctx)


def generate_site(source, target, tpl, ext, ctx=None):
    """Pages: static site generator"""
    pages = [Page(path, source, ext) for path in Page.list(Path(source))]
    if tpl == 'page':
        loader = PackageLoader(tpl)
    else:
        loader = FileSystemLoader(tpl)
    tpl_env = Environment(loader=loader)
    if ctx and not isinstance(ctx, dict):
        ctx = json.loads(ctx)
    if not os.path.exists(target):
        os.makedirs(target)
    ls = sorted(pages, key=lambda x: x.slug)
    ls = sorted(ls, key=lambda x: x.parent or '')

    for p in pages:
        content = render_page(p, ls, tpl_env, ctx)
        write_content(target, path=p.get_absolute_url, content=content)

    ctx.update(pages=date_sort(pages))
    feed = render_any(tpl_env, ctx, tpl='page/feed.xml')
    smap = render_any(tpl_env, ctx, tpl='page/sitemap.xml')
    style = render_any(tpl_env, ctx, tpl='page/style.css')
    write_content(target, path='/feed.xml', content=feed)
    write_content(target, path='/sitemap-pages.xml', content=smap)
    write_content(target, path='/style.css', content=style)


def write_content(static_root, path, content):
    """Utility to write and brotli compress a page
    given a server static root, URL path and page content"""
    no_leading_slash = str(path)[1:]
    full_path = os.path.join(static_root, no_leading_slash)
    if '/' in path[1:]:
        folder = os.path.join(static_root, *path.split('/')[1:-1])
        if not os.path.exists(folder):
            os.makedirs(folder)
    if path.endswith('/') or os.path.isdir(full_path):
        full_path = os.path.join(full_path, 'index.html')
    with open(full_path, 'wb+') as f:
        f.write(content)
    with open(full_path + '.br', 'wb+') as cf:
        compressed = brotli.compress(content)
        cf.write(compressed)


def date_sort(ls):
    return sorted(ls, key=lambda x: x.created, reverse=True)


def get_template(tpl_env, tpl):
    """Fallback"""
    try:
        return tpl_env.get_template(tpl)
    except jinja2.exceptions.TemplateNotFound:
        loader = PackageLoader('page')
        tpl_env = Environment(loader=loader)
        return tpl_env.get_template(tpl)


def render_any(tpl_env, ctx, tpl):
    tpl = get_template(tpl_env, tpl)
    return tpl.render(**ctx).encode()


def render_page(page, ls, tpl_env, ctx, tpl='page/page.html'):
    # nav list from this folder
    in_folder = list(page.list(Path(page.path).parent))
    # pick pages by path out of a full list
    ls = [x for x in ls if x.path in in_folder]
    # pick full parent page object by slug, next(filter(lambda.. is slower
    parent_page = None
    if page.parent:
        parent_page = [x for x in ls if x.slug == page.parent][0]
    # order blog entries by date
    if page.parent == 'blog':
        ls = date_sort(ls)
    if page.home:
        ls = [x for x in ls if not x.parent]
    print(page.get_absolute_url)  # ls[:3]
    ctx.update(page=page, parent_page=parent_page, ls=ls, desc=page.desc)
    return render_any(tpl_env, ctx, tpl)


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
