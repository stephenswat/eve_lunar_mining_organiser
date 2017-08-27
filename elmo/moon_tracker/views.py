from django.shortcuts import render
from django.shortcuts import get_object_or_404
from eve_sde.models import Moon

# Create your views here.
def moon_list(request, region=None, constellation=None, system=None, planet=None):
    pass

def moon_detail(request, system, planet, moon):
    print(system, planet, moon)
    moon_obj = get_object_or_404(Moon, number=moon, planet__number=planet, planet__system__name=system)

    return str(moon_obj)
