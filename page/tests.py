import unittest
from page.models import Page
from pathlib import Path
from page import gen
# from page.imports import *  # add tests
# from page.static import *  # add tests


class PageTestCase(unittest.TestCase):
    def test_model(self):
        """Test a page"""
        p = Page(path=Path('README.md'))
        self.assertEqual(p.slug, 'README')
        self.assertEqual(p.title, 'Page, a static website generator')
        self.assertTrue('<h2>Batteries included' in p.body)

    def test_tpl_loader(self):
        tpls = gen.load_templates('templates')
        self.assertTrue('page.html' in tpls.keys())

    # def test_cli(self):
    #    gen.cli()


if __name__ == '__main__':
    unittest.main()
