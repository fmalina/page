from django.shortcuts import get_object_or_404, render

from .models import Page
from .utils import local_301
from . import app_settings


def page(request, url):
    page = get_object_or_404(Page, url__exact=url)
    ls = Page.objects.all().filter(parent=page.pk).order_by('-created_at')

    if request.get_full_path() != page.get_absolute_url() and\
            'page=' not in request.get_full_path():
        return local_301(page)

    return render(request, 'page/page.html', {
        'page': page,
        'ls': ls,
        'audiences': app_settings.PAGE_AUDIENCE_CHOICES,
        'description': page.desc()
    })


def short(request, pk):
    p = get_object_or_404(Page, pk=pk)
    return local_301(p)


def feed(request):
    pages = Page.objects.all().order_by('-created_at')[:10]
    return render(request, 'page/feed.xml', {'pages': pages},
                  content_type='application/rss+xml')
