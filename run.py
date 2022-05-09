#!/usr/bin/env python3
"""An example program with config to generate your site
Copy it and change variables as needed, so you don't have
to generate your site with a long command."""
from pages.gen import generate_site

ROOT = '/Users/f/SITES/'
SOURCE = f'{ROOT}blocl-pages/'
TARGET = f'{ROOT}blocl/static'
TPL = f'{ROOT}blocl/blocl/templates'
EXT = '.htm'
CTX = dict(
    site_name='Blocl',
    site_url='https://blocl.co'
)

if __name__ == '__main__':
    generate_site(SOURCE, TARGET, TPL, EXT, CTX)
