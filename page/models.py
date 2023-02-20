import os
import time
from dataclasses import dataclass
from datetime import datetime as dt
from email.utils import formatdate
from pathlib import Path

from markdown2 import markdown
from markupsafe import Markup


@dataclass
class Page:
    """
    Markdown files presented as Page objects

    Attributes:
            title (str): <h1> using === or # heading markdown notation
            body (str): whatever follows h1
            slug (str): URL handle from filename without extension
            path (str): initial text file path
            parent (str): parent folder
            created (dt): filesystem time text file was created
            source (str): source folder (top level) used to determine top level pages
            author (str): extracted using "By **author name**" pattern right after heading
            ext (str): empty string, .htm or .html
            home (bool): True for homepage
    """
    title: str
    body: str
    slug: str
    path: str
    parent: str
    created: dt
    source: str
    author: str = ''
    ext: str = ''
    home: bool = False

    def __init__(self, path=None, source='', ext=''):
        if path:
            self.path = path
            self.source = source
            self.ext = ext
            content = open(path).read()
            if content.startswith('#'):
                self.title = content.split('\n')[0].replace('# ', '')
                self.md_body = '\n'.join(content.split('\n')[1:])
            else:
                self.title = content.split('\n===')[0]
                self.md_body = ''.join(content.split('===\n')[1:])
            self.title = self.widont(self.title)
            self.body = markdown(self.md_body, extras=['tables'])
            self.author = ''
            if self.body.startswith('By **'):
                self.author = self.body.split('By **')[-1].split('**')[0]
            self.slug = path.stem
            try:
                self.parent = path.parts[-2]
                if self.slug == 'index':
                    self.slug = self.parent
                    self.parent = None
            except IndexError:
                self.parent = None
            if self.parent == Path(self.source).stem:  # top level
                self.parent = None
            if self.slug == 'index' and not self.parent:  # homepage
                self.home = True
            self.created = dt.fromtimestamp(os.path.getctime(path))

    @staticmethod
    def list(path):
        return list(path.rglob('*.md')) + list(path.rglob('![_assets]*.txt'))


    @staticmethod
    def widont(x):
        """Prevent lonely last word overhanging in a title (widow)"""
        if len(x.split()) > 3:
            return '\u00A0'.join(x.rsplit(' ', 1))
        return x

    @property
    def rfc2822_date(self):
        return formatdate(time.mktime(self.created.timetuple()))

    @property
    def rel_source_path(self):
        return str(self.path).replace(self.source, '')

    @property
    def get_absolute_url(self):
        if self.parent:
            return f'/{self.parent}/{self.slug}{self.ext}'
        elif not self.home:
            return f'/{self.slug}{self.ext}'
        else:
            return '/'

    @property
    def teaser(self):
        if '***' in self.body:
            return self.body.split('\n\n***\n\n')[0]
        return self.body.split('\n\n')[0]

    @property
    def desc(self):
        s = Markup(self.body).striptags()
        return meta_desc(s)

    def __str__(self):
        return self.get_absolute_url

    def __repr__(self):
        return self.get_absolute_url


def meta_desc(s):
    """Generate short description from body"""
    s = " ".join(s.split()[:50])
    limit = 156
    if len(s) <= limit:
        return s
    # cut to size limit, break into words replacing last word with …
    return ' '.join(s.strip()[:limit].split()[:-1]) + '…'
