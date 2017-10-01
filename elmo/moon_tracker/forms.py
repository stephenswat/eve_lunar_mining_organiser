from django import forms

import csv
from io import StringIO

class BatchMoonScanForm(forms.Form):
    data = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control monospace'}),
    )

    def clean(self):
        cleaned_data = super(BatchMoonScanForm, self).clean()
        raw = StringIO(cleaned_data['data'])
        reader = csv.reader(raw, delimiter='\t')

        next(reader)

        res = {}
        current_moon = 0
        percentage_sum = 0
        current_scan = {}

        for x in reader:
            print(x)
            if len(x) == 1:
                if len(x[0]) == 0:
                    raise forms.ValidationError('Invalid input format.')

                if current_moon != 0 and percentage_sum != 100:
                    raise forms.ValidationError('Sum of percentages must be 100.')

                if len(current_scan) > 0 and current_moon != 0:
                    res[current_moon] = current_scan

                current_moon = 0
                percentage_sum = 0
                current_scan = {}
            else:
                if len(x[0]) != 0:
                    raise forms.ValidationError('Invalid input format.')

                moon_id = int(x[6])
                ore_id = int(x[3])
                percentage = int(round(100 * float(x[2])))

                percentage_sum += percentage

                if current_moon == 0:
                    current_moon = moon_id
                elif moon_id != current_moon:
                    raise forms.ValidationError('Unexpected moon ID.')

                if ore_id in current_scan:
                    raise forms.ValidationError('Unexpected moon ID.')

                current_scan[ore_id] = percentage

        print(res)
        cleaned_data['data'] = res
