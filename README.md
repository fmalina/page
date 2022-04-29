Pages, a static website generator
=================================

- creates a well organized website with clear navigation
  reflecting the folder structure of source text documents
- fast, well compressed, mobile friendly pages
- feed and sitemap files for your subscribers and search engines

Writers love distraction free [markdown](https://commonmark.org/help/) under the hood
for formatting source text documents. Template designers love the easy to read,
beautiful and powerful [Jinja2 template language](https://palletsprojects.com/p/jinja/).

Installation and run
--------------------
Pages is a small command line program written in Python programming language.
It requires [python installed](https://www.python.org/downloads/), which lets user
install Pages on any platform in a single command.

    pip3 install git+https://github.com/fmalina/pages.git

By default, Pages will collect all markdown files in current folder
and create a HTML website in a static folder using default templates.

    pages

User can run Pages with custom options like so:

    pages --source /markdown/source/folder/\
          --target /target/folder/\
          --tpl /custom/template/folder/

Batteries included
------------------
Minimal default template.

Pages has lots of (broken) tests including one importing an existing HTML site,
converting it to source markdown files and then back into a static HTML site
in full circle. This code can inspire users to convert existing static site
or one powered by a slow Content Management System to simple
markdown powered static site and maintain it with Pages.

Programmers using Djagno Web Framework can make their sites faster and less demanding
using **static cache generation*** helpers provided, see dj.py.


---

Designed in Slovakia by [Francis Malina](https://unilexicon.com/fm/).
