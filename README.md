Page, a static website generator
================================

- creates a well organized website with clear navigation
  reflecting the folder structure of source text documents
- fast, well compressed, mobile friendly pages
- feed and sitemap files for your subscribers and search engines
- import from any CMS DB (inc. Wordpress), import HTML sites

Writers love distraction free conventional plain text
[formatting](https://commonmark.org/help/).
Template designers love the easy to read, beautiful and powerful
[template language](https://palletsprojects.com/p/jinja/).

Installation and run
--------------------
Page is a small command line program written in Python programming language.
It requires [python installed](https://www.python.org/downloads/), which lets user
install Page on any platform in a single command.

    pip3 install page

By default, Page will collect all text files in current folder
and create a HTML website in a static folder using default templates.

    page

it will look for a config file
[`./page.yml`](https://github.com/fmalina/page/blob/main/page.yml)
with custom options.

    source: /markdown/source/folder/
    target: /target/folder/
    tpl: /custom/template/folder/
    ext: ''  # or '.htm'
    ctx:
        site_name: 'My Site'
        site_url: https://example.org


Batteries included
------------------
Minimal default template.

Page has lots of tests including one importing an existing HTML site,
converting it to source markdown files and then back into a static HTML site
in full circle. This code can inspire users to convert existing static site
or one powered by a slow Content Management System to simple
markdown powered static site and maintain it with Page.

Programmers using Djagno Web Framework can make their sites faster and less demanding
using **static cache generation** helpers provided,
see [static.py](https://github.com/fmalina/page/blob/main/page/static.py).

Example websites using page with sources
----------------------------------------

* [Normy Jedal Food standards](https://unilexicon.com/nom) in Slovak language
        [sources](https://github.com/fmalina/revisions-nom)
* [Sip Sip Herbal Medicine](https://unilexicon.com/sip) in Slovak language
        [sources](https://github.com/fmalina/revisions-sip)
* Blocl [activist literature](https://blocl.uk/activism),
        [blog](https://blocl.uk/blog),
        [privacy policy](https://blocl.uk/privacy)
        [sources](https://github.com/fmalina/revisions-blocl)

Note: public repositories for projects using page begin with word "revisions" to prevent them
from being indexed in public search engines as per [github.com/robots.txt](https://github.com/robots.txt)
---

Designed in Slovakia by [Francis Malina](https://unilexicon.com/fm/).
