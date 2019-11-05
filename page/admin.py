from django.contrib import admin
from .models import Page, Redirect


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'author', 'active', 'updated_at')


@admin.register(Redirect)
class PageAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'usage_count', 'last_used')
