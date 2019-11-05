from django.conf import settings


def soft_404(path):
    """Custom handler to find a new location."""
    return path


PAGE_PARENT_IDS = getattr(settings, 'PAGE_PARENT_IDS', [1, 2, 3])  # e.g. help, blog and press
PAGE_AUDIENCE_CHOICES = getattr(
    settings, 'PAGE_AUDIENCE_CHOICES',
    [('a', 'consenting adults'),
     ('k', 'kids')]
)
PAGE_SOFT_404_LOOKUP_FUNC = gettattr(
    settings, 'PAGE_SOFT_404_LOOKUP_FUNC',
    soft_404
)
PAGE_SOFT_404_MSG = gettattr(
    settings, 'PAGE_SOFT_404_MSG',
    'That listing is gone, here are similar ones.'
)