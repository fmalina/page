from django.test import TestCase
from django.contrib.auth.models import User
from page.models import Page


def create_user():
    u = User.objects.first()
    if not u:
        u = User.objects.create_user('F', 'hi2@blocl.com', 'test*pw')
        u.save()
    return u


class PageTestCase(TestCase):
    def setUp(self):
        """Add a page"""
        create_user()

        p = Page(body='Lorem ipsum...', title='My title')
        p.save()

    def test_model(self):
        """Test a page exists"""
        p = Page.objects.first()
        self.assertEqual(p.pk, 1)
        self.assertEqual(p.slug, 'my-title')
        self.assertEqual(p.title, 'My title')
