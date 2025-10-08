from django import forms
from django.conf import settings
import json
from django.utils import timezone
from .models import DASTScan

class DASTScanForm(forms.ModelForm):
    class Meta:
        model = DASTScan
        fields = ['name', 'target_url', 'scan_type']  # ⭐⭐ HANYA FIELD INI YANG DITAMPILKAN ⭐⭐
        widgets = {
            'scan_type': forms.Select(attrs={'class': 'form-control'}),
            'target_url': forms.URLInput(attrs={'placeholder': 'https://example.com', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'Nama Scan', 'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ⭐⭐ SEMUA FIELD LAINNYA DISEMBUNYIKAN ⭐⭐
        hidden_fields = [
            'vulnerabilities_found', 'pages_crawled', 'requests_made',
            'high_vulnerabilities', 'medium_vulnerabilities',
            'low_vulnerabilities', 'informational_vulnerabilities',
            'scan_date', 'status', 'active', 'scheduled', 'scan_config',
            'completed_date', 'results', 'jenkins_build_number', 'json_report_path'
        ]
        
        for field_name in hidden_fields:
            if field_name in self.fields:
                self.fields[field_name].widget = forms.HiddenInput()
                self.fields[field_name].required = False
    
def clean(self):
    cleaned_data = super().clean()
    
    # ⭐⭐ PERBAIKAN: Enhanced duplicate checking ⭐⭐
    target_url = cleaned_data.get('target_url')
    name = cleaned_data.get('name')
    
    if target_url:
        # Normalize URL untuk avoid false duplicates
        normalized_url = target_url.lower().rstrip('/')
        
        # Cek existing running scans untuk URL yang sama
        existing_running = DASTScan.objects.filter(
            target_url__icontains=normalized_url,
            status='running'
        ).exclude(id=self.instance.id if self.instance else None)
        
        if existing_running.exists():
            raise forms.ValidationError(
                f"Sudah ada scan yang berjalan untuk {target_url}. "
                "Silakan batalkan terlebih dahulu atau tunggu sampai selesai."
            )
        
        # Cek existing pending scans untuk URL yang sama
        existing_pending = DASTScan.objects.filter(
            target_url__icontains=normalized_url,
            status='pending'
        ).exclude(id=self.instance.id if self.instance else None)
        
        if existing_pending.exists():
            raise forms.ValidationError(
                f"Sudah ada scan yang pending untuk {target_url}. "
                "Silakan batalkan terlebih dahulu atau tunggu sampai selesai."
            )
    
    return cleaned_data
