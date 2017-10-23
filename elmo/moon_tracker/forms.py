from django import forms
from moon_tracker.models import ScanResultOre
from django.forms import widgets

from collections import defaultdict
import csv
import math
from io import StringIO


class BatchMoonScanForm(forms.Form):
    data = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control monospace'}),
    )

    def clean(self):
        cleaned_data = super(BatchMoonScanForm, self).clean()

        if 'data' not in cleaned_data:
            raise forms.ValidationError('Input must not be empty.')

        raw = StringIO(cleaned_data['data'])
        reader = csv.reader(raw, delimiter='\t')

        next(reader)

        res = defaultdict(dict)

        for l in reader:
            if len(l) != 7:
                continue

            quantity = float(l[2])
            ore_type = int(l[3])
            moon_id = int(l[6])

            res[moon_id][ore_type] = quantity

        for m, c in res.items():
            if not math.isclose(sum(q for _, q in c.items()), 1.0, abs_tol=0.001):
                raise forms.ValidationError('Sum of quantities must be 1.0.')

        cleaned_data['data'] = res


class FancyMultipleChoiceWidget(widgets.SelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)

        if attrs is None:
            attrs = {}

        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}

        option_attrs = {
            **option_attrs,
            'style': 'background-image: url(https://image.eveonline.com/Type/%d_32.png);' % value
        }

        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)

        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
        }


class OreSearchForm(forms.Form):
    ORE_CHOICES = (
        ('Standard Ores', (
            (46675, 'Dark Ochre'),
            (46676, 'Bistot'),
            (46677, 'Crokite'),
            (46678, 'Arkonor'),
            (46679, 'Gneiss'),
            (46680, 'Hedbergite'),
            (46681, 'Hemorphite'),
            (46682, 'Jaspet'),
            (46683, 'Kernite'),
            (46684, 'Omber'),
            (46685, 'Plagioclase'),
            (46686, 'Pyroxeres'),
            (46687, 'Scordite'),
            (46688, 'Spodumain'),
            (46689, 'Veldspar'),
        )),
        ('Moon Ores', (
            (45490, 'Zeolites'),
            (45491, 'Sylvites'),
            (45492, 'Bitumens'),
            (45493, 'Coesite'),

            (45494, 'Cobaltite'),
            (45495, 'Euxenite'),
            (45496, 'Titanite'),
            (45497, 'Scheelite'),

            (45498, 'Otavite'),
            (45499, 'Sperrylite'),
            (45500, 'Vanadinite'),
            (45501, 'Chromite'),

            (45502, 'Carnotite'),
            (45503, 'Zircon'),
            (45504, 'Pollucite'),
            (45506, 'Cinnabar'),

            (45510, 'Xenotime'),
            (45511, 'Monazite'),
            (45512, 'Loparite'),
            (45513, 'Ytterbite'),
        )),
    )


    ore_type = forms.MultipleChoiceField(
        choices=ORE_CHOICES,
        widget=FancyMultipleChoiceWidget()
    )

    min_quantity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={'type':'range', 'step': '0.01', 'min': '0.0', 'max': '1.0'}
        )
    )

    def clean(self):
        cleaned_data = super(OreSearchForm, self).clean()
        cleaned_data['ore_type'] = [int(x) for x in cleaned_data.get('ore_type', [])]
