from django import forms
from django.core.exceptions import ValidationError
from .models import UserSCMProfile, ScanJob, ScanSchedule, Repository

class SCMProfileForm(forms.ModelForm):
    """Enhanced SCM Profile Form with better validation and security"""
    
    # Field untuk konfirmasi token (optional)
    confirm_access_token = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=True),
        label="Confirm Access Token",
        help_text="Optional: Re-enter token to confirm"
    )
    
    class Meta:
        model = UserSCMProfile
        fields = ['scm_type', 'access_token', 'api_url', 'username', 'is_active']
        widgets = {
            'access_token': forms.PasswordInput(render_value=True, attrs={
                'placeholder': 'Enter your access token...',
                'class': 'form-control'
            }),
            'api_url': forms.URLInput(attrs={
                'placeholder': 'https://api.github.com (optional for GitHub)',
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Your SCM username',
                'class': 'form-control'
            }),
            'scm_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        help_texts = {
            'access_token': 'GitHub: personal access token, GitLab: private token, Bitbucket: app password',
            'api_url': 'Custom API URL (e.g., https://gitlab.company.com/api/v4 for self-hosted GitLab)',
            'username': 'Your username on the SCM platform',
        }
    
    def clean_access_token(self):
        token = self.cleaned_data.get('access_token')
        if not token:
            raise ValidationError("Access token is required")
        
        if len(token) < 10:
            raise ValidationError("Access token seems too short. Please check your token.")
        
        # Basic validation based on scm_type
        scm_type = self.cleaned_data.get('scm_type')
        if scm_type == 'github' and not token.startswith(('ghp_', 'github_pat_')):
            raise ValidationError("GitHub tokens usually start with 'ghp_' or 'github_pat_'")
        
        return token
    
    def clean_confirm_access_token(self):
        confirm_token = self.cleaned_data.get('confirm_access_token')
        token = self.cleaned_data.get('access_token')
        
        if confirm_token and confirm_token != token:
            raise ValidationError("Access tokens do not match")
        
        return confirm_token
    
    def clean_api_url(self):
        api_url = self.cleaned_data.get('api_url')
        scm_type = self.cleaned_data.get('scm_type')
        
        if api_url:
            # Validate API URL format
            if not api_url.startswith(('http://', 'https://')):
                raise ValidationError("API URL must start with http:// or https://")
            
            # Set default API URLs if empty based on scm_type
            if scm_type == 'github' and not api_url:
                api_url = 'https://api.github.com'
            elif scm_type == 'gitlab' and not api_url:
                api_url = 'https://gitlab.com/api/v4'
            elif scm_type == 'bitbucket' and not api_url:
                api_url = 'https://api.bitbucket.org/2.0'
        
        return api_url
    
    def clean(self):
        cleaned_data = super().clean()
        scm_type = cleaned_data.get('scm_type')
        username = cleaned_data.get('username')
        
        # Validate username based on SCM type
        if scm_type and username:
            if scm_type == 'github':
                # GitHub username validation
                if len(username) > 39:
                    raise ValidationError({
                        'username': 'GitHub username cannot exceed 39 characters'
                    })
                if not all(c.isalnum() or c == '-' for c in username):
                    raise ValidationError({
                        'username': 'GitHub username can only contain alphanumeric characters and hyphens'
                    })
            elif scm_type == 'gitlab':
                # GitLab username validation
                if len(username) > 255:
                    raise ValidationError({
                        'username': 'GitLab username cannot exceed 255 characters'
                    })
        
        return cleaned_data

    # forms.py - PERBAIKI ScanForm untuk filter by SCM type

class ScanForm(forms.ModelForm):
    """Enhanced Scan Form dengan SCM type filtering"""
    
    scan_type = forms.ChoiceField(
        choices=[
            ('full', 'Full Scan - All rules'),
            ('security', 'Security Audit - Security-focused rules'),
            ('secrets', 'Secrets Detection - API keys, tokens, etc.'),
            ('ci', 'CI Scan - Fast scan for CI/CD'),
            ('custom', 'Custom Rules - Use custom rules only'),
        ],
        initial='full',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'scan-type-select'
        }),
        help_text="Select the type of security scan to perform"
    )
    
    # ✅ TAMBAH FIELD UNTUK FILTER SCM TYPE
    scm_type_filter = forms.ChoiceField(
        choices=[
            ('all', 'All SCM Types'),
            ('github', 'GitHub Repositories'),
            ('gitlab', 'GitLab Repositories'), 
            ('bitbucket', 'Bitbucket Repositories'),
        ],
        required=False,
        initial='all',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'scm-type-filter'
        }),
        help_text="Filter repositories by SCM type"
    )
    
    custom_rules = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Paste your custom Semgrep rules in YAML format...',
            'class': 'form-control',
            'rows': 6,
            'style': 'font-family: monospace; font-size: 12px;'
        }),
        help_text="Optional: Custom Semgrep rules in YAML format"
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Filter repositories based on user permissions
        if user.is_superuser:
            repositories = Repository.objects.filter(is_active=True)
        else:
            scm_profiles = UserSCMProfile.objects.filter(user=user, is_active=True)
            repositories = Repository.objects.filter(
                scm_profile__in=scm_profiles, 
                is_active=True
            ).select_related('scm_profile')
        
        # ✅ APPLY SCM TYPE FILTER JIKA ADA
        scm_type = self.data.get('scm_type_filter') if self.data else None
        if scm_type and scm_type != 'all':
            repositories = repositories.filter(scm_profile__scm_type=scm_type)
            print(f"🔍 Filtering repositories by SCM type: {scm_type}")
        
        # Update repository field dengan filtered queryset
        self.fields['repository'].queryset = repositories
        self.fields['repository'].empty_label = "Select a repository"
        self.fields['repository'].widget.attrs.update({
            'class': 'form-control',
            'id': 'repository-select'
        })
        
        # Set initial values
        self.fields['branch'].initial = 'main'
        self.fields['branch'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'main, develop, feature/branch-name'
        })
        
        # Add repository count information
        self.repository_count = repositories.count()
        self.available_scm_types = list(repositories.values_list(
            'scm_profile__scm_type', flat=True
        ).distinct())
    
    class Meta:
        model = ScanJob
        fields = ['repository', 'branch']
        widgets = {
            'branch': forms.TextInput(attrs={
                'placeholder': 'main, develop, feature/*'
            }),
        }
        help_texts = {
            'repository': 'Select the repository to scan',
            'branch': 'Specify the branch to scan (default: main)',
        }
    
    # ... existing clean methods tetap sama ...    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Filter repositories based on user permissions
        if user.is_superuser:
            repositories = Repository.objects.filter(is_active=True)
        else:
            scm_profiles = UserSCMProfile.objects.filter(user=user, is_active=True)
            repositories = Repository.objects.filter(
                scm_profile__in=scm_profiles, 
                is_active=True
            ).select_related('scm_profile')
        
        # Update repository field with filtered queryset
        self.fields['repository'].queryset = repositories
        self.fields['repository'].empty_label = "Select a repository"
        self.fields['repository'].widget.attrs.update({
            'class': 'form-control',
            'id': 'repository-select'
        })
        
        # Set initial values
        self.fields['branch'].initial = 'main'
        self.fields['branch'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'main, develop, feature/branch-name'
        })
        
        # Add repository count information
        self.repository_count = repositories.count()
    
    class Meta:
        model = ScanJob
        fields = ['repository', 'branch']
        widgets = {
            'branch': forms.TextInput(attrs={
                'placeholder': 'main, develop, feature/*'
            }),
        }
        help_texts = {
            'repository': 'Select the repository to scan',
            'branch': 'Specify the branch to scan (default: main)',
        }
    
    def clean_repository(self):
        repository = self.cleaned_data.get('repository')
        
        if not repository:
            raise ValidationError("Please select a repository")
        
        # Check if user has access to this repository
        if not self.user.is_superuser:
            user_scm_profiles = UserSCMProfile.objects.filter(user=self.user, is_active=True)
            if repository.scm_profile not in user_scm_profiles:
                raise ValidationError("You don't have permission to scan this repository")
        
        return repository
    
    def clean_branch(self):
        branch = self.cleaned_data.get('branch')
        
        if not branch:
            raise ValidationError("Branch name is required")
        
        # Basic branch name validation
        if len(branch) > 200:
            raise ValidationError("Branch name is too long")
        
        if not all(c.isalnum() or c in ['-', '_', '/', '.'] for c in branch):
            raise ValidationError("Branch name contains invalid characters")
        
        return branch
    
    def clean_custom_rules(self):
        custom_rules = self.cleaned_data.get('custom_rules')
        scan_type = self.cleaned_data.get('scan_type')
        
        if scan_type == 'custom' and not custom_rules:
            raise ValidationError("Custom rules are required when selecting 'Custom Rules' scan type")
        
        if custom_rules:
            # Basic YAML validation
            try:
                import yaml
                yaml.safe_load(custom_rules)
            except Exception as e:
                raise ValidationError(f"Invalid YAML format in custom rules: {str(e)}")
        
        return custom_rules
    
    def clean(self):
        cleaned_data = super().clean()
        repository = cleaned_data.get('repository')
        
        # Check if repository is active
        if repository and not repository.is_active:
            raise ValidationError({
                'repository': 'This repository is not active. Please contact administrator.'
            })
        
        return cleaned_data

class ScanScheduleForm(forms.ModelForm):
    """Enhanced Form for managing scan schedules with validation"""
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Filter repositories based on user permissions
        if user.is_superuser:
            repositories = Repository.objects.filter(is_active=True)
        else:
            scm_profiles = UserSCMProfile.objects.filter(user=user, is_active=True)
            repositories = Repository.objects.filter(
                scm_profile__in=scm_profiles, 
                is_active=True
            )
        
        self.fields['repository'].queryset = repositories
        self.fields['repository'].empty_label = "Select a repository"
        
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
    
    class Meta:
        model = ScanSchedule
        fields = ['name', 'repository', 'frequency', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Daily Security Scan, Weekly Audit, etc.',
                'class': 'form-control'
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        help_texts = {
            'name': 'Descriptive name for this schedule',
            'repository': 'Repository to scan on schedule',
            'frequency': 'How often to run the scan',
            'is_active': 'Enable or disable this schedule',
        }
        labels = {
            'is_active': 'Active Schedule'
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError("Schedule name is required")
        
        if len(name) < 3:
            raise ValidationError("Schedule name must be at least 3 characters long")
        
        # Check for duplicate schedule names for this user
        existing = ScanSchedule.objects.filter(
            user=self.user, 
            name=name
        )
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise ValidationError("You already have a schedule with this name")
        
        return name
    
    def clean_repository(self):
        repository = self.cleaned_data.get('repository')
        
        if not repository:
            raise ValidationError("Please select a repository")
        
        # Check if user has access to this repository
        if not self.user.is_superuser:
            user_scm_profiles = UserSCMProfile.objects.filter(user=self.user, is_active=True)
            if repository.scm_profile not in user_scm_profiles:
                raise ValidationError("You don't have permission to schedule scans for this repository")
        
        return repository

class RepositorySyncForm(forms.Form):
    """Form for manually syncing repositories from SCM"""
    
    scm_profile = forms.ModelChoiceField(
        queryset=UserSCMProfile.objects.none(),
        empty_label="Select SCM Profile",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select which SCM profile to sync repositories from"
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Filter SCM profiles for this user
        if user.is_superuser:
            scm_profiles = UserSCMProfile.objects.filter(is_active=True)
        else:
            scm_profiles = UserSCMProfile.objects.filter(user=user, is_active=True)
        
        self.fields['scm_profile'].queryset = scm_profiles
    
    def clean_scm_profile(self):
        scm_profile = self.cleaned_data.get('scm_profile')
        
        if not scm_profile:
            raise ValidationError("Please select an SCM profile")
        
        # Verify user has access to this SCM profile
        if not self.user.is_superuser and scm_profile.user != self.user:
            raise ValidationError("You don't have permission to access this SCM profile")
        
        return scm_profile

class VulnerabilityFilterForm(forms.Form):
    """Form for filtering vulnerabilities in reports"""
    
    SEVERITY_CHOICES = [
        ('all', 'All Severities'),
        ('CRITICAL', 'Critical'),
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
        ('INFO', 'Info'),
    ]
    
    CONFIDENCE_CHOICES = [
        ('all', 'All Confidence Levels'),
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]
    
    severity = forms.ChoiceField(
        choices=SEVERITY_CHOICES,
        initial='all',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    confidence = forms.ChoiceField(
        choices=CONFIDENCE_CHOICES,
        initial='all',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    file_path = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by file path...'
        })
    )
    
    false_positive = forms.ChoiceField(
        choices=[
            ('all', 'All'),
            ('true', 'False Positives Only'),
            ('false', 'Exclude False Positives'),
        ],
        initial='false',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ScanJobFilterForm(forms.Form):
    """Form for filtering scan jobs"""
    
    STATUS_CHOICES = [
        ('all', 'All Statuses'),
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        initial='all',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    repository = forms.ModelChoiceField(
        queryset=Repository.objects.none(),
        required=False,
        empty_label="All Repositories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_range = forms.ChoiceField(
        choices=[
            ('all', 'All Time'),
            ('today', 'Today'),
            ('week', 'This Week'),
            ('month', 'This Month'),
        ],
        initial='all',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter repositories based on user
        if user.is_superuser:
            repositories = Repository.objects.filter(is_active=True)
        else:
            scm_profiles = UserSCMProfile.objects.filter(user=user, is_active=True)
            repositories = Repository.objects.filter(
                scm_profile__in=scm_profiles, 
                is_active=True
            )
        
        self.fields['repository'].queryset = repositories
