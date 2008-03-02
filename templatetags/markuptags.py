from django.template import Library
from markup_utils.filters import markup_chain
from django.utils.safestring import mark_safe

register = Library()

@register.filter('markup_chain')
def do_markup_chain(value):
    return mark_safe(markup_chain(value))

