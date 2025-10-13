from django import forms
from .models import DarkWebScan

class DarkWebScanForm(forms.ModelForm):
    class Meta:
        model = DarkWebScan
        fields = ['target', 'scan_type']
        widgets = {
            'target': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company domain or email address'
            }),
            'scan_type': forms.Select(attrs={'class': 'form-control'})
        }
