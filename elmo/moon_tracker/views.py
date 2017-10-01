from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.forms import inlineformset_factory, NumberInput, Select

from eve_sde.models import Region, Constellation, SolarSystem, Moon
from moon_tracker.utils import user_can_view_scans, user_can_add_scans, user_can_delete_scans
from moon_tracker.models import ScanResult, ScanResultOre
from moon_tracker.forms import BatchMoonScanForm

def list_universe(request):
    regions = (
        Region.objects
        .filter(id__lt=11000000)
        .filter(constellations__systems__security__lt=0.5)
        .annotate(num_moons=Count('constellations__systems__planets__moons'))
        .order_by('name')
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
        .filter(systems__security__lt=0.5)
        .annotate(num_moons=Count('systems__planets__moons'))
        .order_by('name')
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
        .filter(security__lt=0.5)
        .annotate(num_moons=Count('planets__moons'))
        .order_by('name')
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
    form = ScanResultOreFormSet = inlineformset_factory(
        ScanResult,
        ScanResultOre,
        fields=('ore', 'percentage'),
        can_delete=False,
        widgets={
            'ore': Select(attrs={'class': 'custom-select form-control ore-type-input'}),
            'percentage': NumberInput(attrs={'value': 0, 'max': 100, 'class': 'form-control ore-percentage-input'})
        }
    )

    return render(
        request,
        'moon_tracker/moon_detail.html',
        context={
            'moon': moon_obj,
            'can_view': user_can_view_scans(request.user, moon_obj),
            'can_add': user_can_add_scans(request.user, moon_obj),
            'can_delete': user_can_delete_scans(request.user, moon_obj),
            'form': form
        }
    )

def batch_submit(request):
    if request.method == 'POST':
        form = BatchMoonScanForm(request.POST)

        if form.is_valid():
            for moon, materials in form.cleaned_data['data'].items():
                result = ScanResult.objects.create(
                    moon_id=moon,
                    owner=request.user
                )

                for ore, percentage in materials.items():
                    result.constituents.create(
                        ore=ore,
                        percentage=percentage
                    )

            return redirect('/')
    else:
        form = BatchMoonScanForm()

    return render(request, 'moon_tracker/batch_submit.html', {'form': form})
