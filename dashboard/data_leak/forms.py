from django import forms
from .models import DataLeakScan

class DataLeakScanForm(forms.ModelForm):
    class Meta:
        model = DataLeakScan
        fields = ['target', 'scan_type']
        widgets = {
            'target': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter domain or email to scan'
            }),
            'scan_type': forms.Select(attrs={'class': 'form-control'})
        }
