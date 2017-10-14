from django import forms
from moon_tracker.models import ScanResultOre, ORE_CHOICES
from django.forms import widgets

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

        res = {}
        current_moon = 0
        quantity_sum = 0.0
        current_scan = {}

        for x in reader:
            if len(x) == 1:
                if len(x[0]) == 0:
                    raise forms.ValidationError('Invalid input format.')

                if current_moon != 0 and not math.isclose(quantity_sum, 1.0, abs_tol=0.001):
                    raise forms.ValidationError('Sum of quantities must be 1.0.')

                if len(current_scan) > 0 and current_moon != 0:
                    res[current_moon] = current_scan

                current_moon = 0
                quantity_sum = 0.0
                current_scan = {}
            else:
                if len(x[0]) != 0:
                    raise forms.ValidationError('Invalid input format.')

                moon_id = int(x[6])
                ore_id = int(x[3])
                quantity = float(x[2])

                quantity_sum += quantity

                if current_moon == 0:
                    current_moon = moon_id
                elif moon_id != current_moon:
                    raise forms.ValidationError('Unexpected moon ID.')

                if ore_id in current_scan:
                    raise forms.ValidationError('Unexpected moon ID.')

                current_scan[ore_id] = quantity

        print(res)
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
