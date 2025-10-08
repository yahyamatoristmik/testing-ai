# ==========================================
# message/forms.py
# ==========================================
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone', 'company', 'subject', 'service', 'message']
    
    def __init__(self, *args, **kwargs):  # Perbaiki dari **init**
        super().__init__(*args, **kwargs)
        
        # Customize form fields
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'required': True
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'your.email@company.com',
            'required': True
        })
        
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '+62 (852) 123-4567 (optional)'
        })
        
        self.fields['company'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your company name (optional)'
        })
        
        self.fields['subject'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Brief subject of your message',
            'required': True
        })
        
        self.fields['service'].widget.attrs.update({
            'class': 'form-select'
        })
        
        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Describe your project or inquiry in detail...',
            'rows': 5,
            'required': True
        })
