from urllib.parse import urlencode
from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def page_replace(context, new_page, page_name="page"):
    query = dict(context['request'].GET)
    query[page_name] = new_page
    return urlencode(query, doseq=True)
