import json
import os
import shutil
from pathlib import Path
import brotli
import yaml
from minijinja import Environment
from page.models import Page


def cli():
    try:
        f = open('page.yml', 'r')
        d = yaml.safe_load(f)
    except FileNotFoundError:
        print('No page.yml file, using defaults.')
        d = {}
    source = d.get('source', '.')
    target = d.get('target', '_static')
    tpl = d.get('tpl', 'page')
    ext = d.get('ext', '')
    ctx = d.get('ctx', {})
    generate_site(source, target, tpl, ext, ctx)


def load_templates(user_tpl_dir):
    tpls = list(Path(__file__).parent.glob('templates/*'))\
           + list(Path(user_tpl_dir).glob('*'))
    return {x.name: x.read_text() for x in tpls}


def render_tpl(env, ctx, tpl):
    return env.render_template(tpl, **ctx).encode()


def generate_site(source, target, tpl, ext, ctx=None):
    """Pages: static site generator"""
    pages = [Page(path, source, ext) for path in Page.list(Path(source))]

    env = Environment(templates=load_templates(tpl))
    if ctx and not isinstance(ctx, dict):
        ctx = json.loads(ctx)
    if not os.path.exists(target):
        os.makedirs(target)
    ls = sorted(pages, key=lambda x: x.slug)
    ls = sorted(ls, key=lambda x: x.parent or '')

    for p in pages:
        content = render_page(p, ls, env, ctx, tpl='page.html')
        write_content(target, path=p.get_absolute_url, content=content)

    ctx.update(pages=date_sort(pages))
    feed = render_tpl(env, ctx, tpl='feed.xml')
    smap = render_tpl(env, ctx, tpl='sitemap.xml')
    write_content(target, path='/feed.xml', content=feed)
    write_content(target, path='/sitemap-pages.xml', content=smap)

    if 'shop' in tpl:  # shop specific order form rendering
        # this may need expanding for other theme specific html files
        order = render_tpl(env, ctx, tpl='order.htm')
        write_content(target, path='/order.htm', content=order)
        order2 = render_tpl(env, ctx, tpl='order.php')
        write_content(target, path='/order.php', content=order2)

    print('copying assets..')
    tpl_assets = __file__.replace('gen.py', 'templates')
    for assets in (
        os.path.join(tpl_assets, tpl, '_assets'),  # template assets
        os.path.join(source, '_assets'),  # project assets to override tpl assets
    ):
        if os.path.exists(assets):
            shutil.copytree(assets, target, dirs_exist_ok=True)


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
    # brotli compress if not a raster image
    if full_path[-4:] not in ('webp', 'jpeg', '.jpg', '.png', '.gif'):
        with open(full_path + '.br', 'wb+') as cf:
            compressed = brotli.compress(content)
            cf.write(compressed)


def date_sort(ls):
    return sorted(ls, key=lambda x: x.created, reverse=True)


def render_page(page, ls, tpl_env, ctx, tpl):
    # nav list from this folder
    in_folder = list(page.list(Path(page.path).parent))
    # pick pages by path out of a full list
    ls = [x for x in ls if x.path in in_folder]
    # pick full parent page object by slug, next(filter(lambda.. is slower
    parent_page = None
    if page.parent:
        parent_page = [x for x in ls if x.slug == page.parent][0]
    # remove parent page from current sibling nav list
    if not parent_page:
        ls.remove(page)
    else:
        ls.remove(parent_page)
    # order blog entries by date
    if page.parent == 'blog':
        ls = date_sort(ls)
    if page.home:
        ls = [x for x in ls if not x.parent]
    print(page.get_absolute_url)  # ls[:3]
    ctx.update(page=page, parent_page=parent_page, ls=ls, desc=page.desc)
    return render_tpl(tpl_env, ctx, tpl)


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
