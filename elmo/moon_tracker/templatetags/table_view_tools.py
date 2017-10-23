from django import template


register = template.Library()


@register.filter()
def get_ore(d, k):
    return d[k]
