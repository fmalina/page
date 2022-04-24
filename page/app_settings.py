from django.conf import settings


def soft_404(path):
    """Custom handler to find a new location."""
    return


PAGE_PARENT_IDS = getattr(settings, 'PAGE_PARENT_IDS', [1, 2, 3])  # e.g. help, blog and press

PAGE_SOFT_404_LOOKUP_FUNC = getattr(
    settings, 'PAGE_SOFT_404_LOOKUP_FUNC',
    soft_404
)
PAGE_SOFT_404_MSG = getattr(
    settings, 'PAGE_SOFT_404_MSG',
    'That listing is gone, here are similar ones.'
)
