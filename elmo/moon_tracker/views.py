from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count

from eve_sde.models import Region, Constellation, SolarSystem, Moon

def list_universe(request):
    regions = (
        Region.objects
        .filter(id__lt=11000000)
        .annotate(num_moons=Count('constellations__systems__planets__moons'))
    )

    return render(
        request,
        'moon_tracker/grid_list.html',
        context={
            'items': regions,
            'parent': None,
            'type': 'universe'
        }
    )

def list_region(request, region):
    region_obj = get_object_or_404(Region, name=region)
    constellations = (
        Constellation.objects
        .filter(region=region_obj)
        .annotate(num_moons=Count('systems__planets__moons'))
    )

    return render(
        request,
        'moon_tracker/grid_list.html',
        context={
            'items': constellations,
            'parent': region_obj,
            'type': 'region'
        }
    )

def list_constellation(request, constellation):
    constellation_obj = get_object_or_404(Constellation, name=constellation)
    systems = (
        SolarSystem.objects
        .filter(constellation=constellation_obj)
        .annotate(num_moons=Count('planets__moons'))
    )

    return render(
        request,
        'moon_tracker/grid_list.html',
        context={
            'items': systems,
            'parent': constellation_obj,
            'type': 'constellation'
        }
    )

def list_system(request, system):
    system_obj = get_object_or_404(SolarSystem, name=system)

    return render(
        request,
        'moon_tracker/system_list.html',
        context={
            'parent': system_obj,
            'type': 'system'
        }
    )

def moon_detail(request, system, planet, moon):
    moon_obj = get_object_or_404(Moon, number=moon, planet__number=planet, planet__system__name=system)

    return render(
        request,
        'moon_tracker/moon_detail.html',
        context={
            'moon': moon_obj
        }
    )
