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

        res = []

        for x in reader:
            print(x)
            if len(x) == 1:
                assert(len(x[0]) > 0)

                current_moon = 0
                current_scan = {}
                res.append(current_scan)
            else:
                assert(len(x[0]) == 0)

                moon_id = int(x[6])
                ore_id = int(x[3])
                percentage = int(round(100 * float(x[2])))

                if current_moon == 0:
                    current_moon = moon_id
                else:
                    assert(moon_id == current_moon)

                assert(ore_id not in current_scan)

                current_scan[ore_id] = percentage

        print(res)
        cleaned_data['data'] = res
