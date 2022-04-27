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
    """Markdown files presented as Page objects"""
    title: str
    body: str
    slug: str
    path: str
    parent: str
    created: dt
    author: str = ''

    def __init__(self, path=None):
        if path:
            self.path = path
            content = open(path).read()
            self.title = self.widont(content.split('\n===')[0])
            self.md_body = content.split('===\n')[-1]
            self.body = markdown(self.md_body)
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
            self.created = dt.fromtimestamp(os.path.getctime(path))

    @staticmethod
    def list(path):
        return Path(path).parent.rglob('*.md')

    @staticmethod
    def widont(x):
        """Prevent lonely last word overhanging in a title (widow)"""
        return '\u00A0'.join(x.rsplit(' ', 1))

    @property
    def rfc2822_date(self):
        return formatdate(time.mktime(self.created.timetuple()))

    @property
    def get_absolute_url(self):
        if self.parent:
            return f'/{self.parent}/{self.slug}'
        else:
            return f'/{self.slug}'

    def teaser(self):
        return self.body.split('\n\n***\n\n')[0]

    @property
    def desc(self):
        """Generate short description from initial paragraphs"""
        s = Markup(self.body).striptags()
        s = " ".join(s.split()[:50])
        limit = 156
        if len(s) <= limit:
            return s
        # cut to size limit, break into words replacing last word with …
        return ' '.join(s.strip()[:limit].split()[:-1]) + '…'

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.get_absolute_url
