from jinja2 import Environment, PackageLoader
from pathlib import Path

env = Environment(loader=PackageLoader("fpage"))


def render_page(page):
    tpl = env.get_template('page/page.html')
    ls = page.list(Path(page.path).parent, date_order=page.date_order)
    return tpl.render(page=page, ls=ls, desc=page.desc())


def render_feed(pages):
    tpl = env.get_template('page/feed.xml')
    return tpl.render(pages=pages)
