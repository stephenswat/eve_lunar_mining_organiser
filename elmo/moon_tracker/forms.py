from django import forms

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
