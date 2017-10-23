from django import template


register = template.Library()


@register.filter()
def get_mineral_dict(d, k):
    return d.get(k, {})


@register.filter()
def get_ore(d, k):
    return d.get(k, None)
