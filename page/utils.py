from django.conf import settings
from django.shortcuts import redirect
from django.template.defaultfilters import truncatewords, striptags


def meta_desc(body, title):
    """Generate meta description out of body and title."""
    body = striptags(truncatewords(body, 50))  # strip tags & newlines
    s = f'{body} - {title}'  # body alone can be too short
    limit = 156
    if len(s) <= limit:
        return s
    s = s.strip()[:limit]  # cut to size
    words = s.split(' ')[:-1]  # break into words and remove the last
    return ' '.join(words) + '…'


def local_301(o):
    return redirect(settings.SITE_URL + o.get_absolute_url(), permanent=True)
