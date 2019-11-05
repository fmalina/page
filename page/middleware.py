from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect

from .models import Redirect
from .views import page
from . import app_settings


def fallback_middleware(get_response):
    def middleware(request):
        path = request.get_full_path()
        response = get_response(request)
        if response.status_code not in (404,410,301):
            return response
        try:
            slug = path.split('?')[0]
            slug = slug.split('/')[-1]
            return page(request, slug)
        except Http404:
            try:
                r = Redirect.objects.get(old_path=path)
                if not r.new_path:
                    r.new_path = '/'
                new = r.new_path
                if not new.startswith('http'):
                    new = settings.SITE_URL+new
                r.usage_count += 1
                r.last_used = datetime.now()
                r.save()
                return redirect(new, permanent=True)
            except Redirect.DoesNotExist:
                goto = app_settings.PAGE_SOFT_404_LOOKUP_FUNC(path)
                if goto:
                    messages.success(request, app_settings.PAGE_SOFT_404_MSG)
                    return redirect(settings.SITE_URL+'/'+goto, permanent=True)
        return response
    return middleware
