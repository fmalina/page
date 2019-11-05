from django.template import Library

register = Library()


@register.filter
def widont(x):
    return '\u00A0'.join(x.rsplit(' ', 1))
