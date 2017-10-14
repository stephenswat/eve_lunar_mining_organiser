from urllib.parse import urlencode
from django import template
from moon_tracker.models import get_ore_name_from_id


register = template.Library()


@register.filter()
def ore_id_to_name(oid):
    return get_ore_name_from_id(oid)
