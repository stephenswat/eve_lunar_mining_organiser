from django import template


register = template.Library()


@register.inclusion_tag('moon_tracker/scan_result.html')
def display_scan(scan):
    return {'scan': scan}
