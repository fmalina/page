from unittest import TestCase
from page.models import Page


class PageTestCase(TestCase):
    def test_model(self):
        """Test a page"""
        p = Page(body='Lorem ipsum...', title='My title', slug='my-title')
        self.assertEqual(p.slug, 'my-title')
        self.assertEqual(p.title, 'My title')
