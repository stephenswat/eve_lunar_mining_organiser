from django import forms

class BatchMoonScanForm(forms.Form):
    data = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control monospace'}),
    )
